from typing import Any, Dict

import yfinance as yf
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


MODEL = LiteLlm(model="openai/gpt-4o")


def _error_response(ticker: str, message: str) -> Dict[str, Any]:
    """공통 에러 응답 포맷."""
    return {
        "ticker": ticker,
        "success": False,
        "error": message,
    }


def get_company_info(ticker: str) -> Dict[str, Any]:
    """
    지정한 티커에 대한 기본 기업 정보를 조회합니다.

    야후 파이낸스에서 공식 기업명, 산업 분류, 섹터 정보를 수집해 기초 프로필을 제공합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - company_name (str): 기업의 정식 명칭
            - industry (str): 세부 산업군
            - sector (str): 상위 섹터 구분

    Example:
        >>> get_company_info('MSFT')
        {
            'ticker': 'MSFT',
            'success': True,
            'company_name': 'Microsoft Corporation',
            'industry': 'Software - Infrastructure',
            'sector': 'Technology'
        }
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
    except Exception as exc:  # pragma: no cover - 네트워크 의존
        return _error_response(ticker, f"회사 정보 조회 실패: {exc}")

    if not info:
        return _error_response(ticker, "회사 정보를 찾을 수 없습니다.")
    return {
        "ticker": ticker,
        "success": True,
        "company_name": info.get("longName", "NA"),
        "industry": info.get("industry", "NA"),
        "sector": info.get("sector", "NA"),
    }


def get_stock_price(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """
    지정된 기간의 주가 이력과 현재가를 동시에 제공합니다.

    시가·고가·저가·종가·거래량이 포함된 히스토리와 실시간 시세를 함께 반환합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')
        period (str): 가격 이력을 조회할 기간. 사용 가능 옵션:
            - '1d': 1일
            - '5d': 5일
            - '1mo': 1개월(기본값)
            - '3mo': 3개월
            - '6mo': 6개월
            - '1y': 1년
            - '2y': 2년
            - '5y': 5년
            - '10y': 10년
            - 'ytd': 연초 이후
            - 'max': 제공 가능한 최대 기간

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - history (str): OHLCV가 담긴 JSON 형식의 가격 이력
            - current_price (float): 현재 시장 가격

    Example:
        >>> get_stock_price('TSLA', '3mo')
        {
            'ticker': 'TSLA',
            'success': True,
            'history': '{"Open": {...}, "High": {...}, ...}',
            'current_price': 245.67
        }
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        history = stock.history(period=period)
    except Exception as exc:  # pragma: no cover - 네트워크 의존
        return _error_response(ticker, f"주가 데이터 조회 실패: {exc}")

    if history is None or history.empty:
        return _error_response(ticker, f"{period} 기간에 대한 주가 이력이 없습니다.")

    current_price = info.get("currentPrice")
    if current_price is None:
        try:
            current_price = float(history["Close"].dropna().iloc[-1])
        except (KeyError, IndexError):
            current_price = None

    history_json = history.to_json()

    close_series = history.get("Close")
    price_summary = {}
    if close_series is not None and not close_series.dropna().empty:
        recent_close = float(close_series.dropna().iloc[-1])
        first_close = float(close_series.dropna().iloc[0])
        change_pct = ((recent_close - first_close) / first_close * 100) if first_close else None
        price_summary = {
            "latest_close": recent_close,
            "change_pct": change_pct,
            "period_candles": int(close_series.shape[0]),
        }
    return {
        "ticker": ticker,
        "success": True,
        "history": history_json,
        "current_price": current_price,
        "price_summary": price_summary,
        "period": period,
    }


def get_financial_metrics(ticker: str) -> Dict[str, Any]:
    """
    주식 분석에 필요한 핵심 재무 지표와 밸류에이션 비율을 제공합니다.

    기업 가치평가, 수익성, 배당 정책, 시장 변동성 등을 판단하는 주요 지표를 모읍니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - market_cap (float): 시가총액(USD)
            - pe_ratio (float): 주가수익비율(PER)
            - dividend_yield (float): 연 배당수익률(0.02 = 2%)
            - beta (float): 시장 대비 변동성을 나타내는 베타값

    Notes:
        - 시가총액: 발행주식수 × 주가
        - PER: 낮을수록 저평가, 높을수록 성장 기대를 의미할 수 있습니다.
        - 배당수익률: 주가 대비 연간 배당금 비율
        - 베타: 1 미만이면 시장보다 덜, 1 초과면 더 민감하게 움직입니다.

    Example:
        >>> get_financial_metrics('JNJ')
        {
            'ticker': 'JNJ',
            'success': True,
            'market_cap': 385000000000,
            'pe_ratio': 15.2,
            'dividend_yield': 0.031,
            'beta': 0.65
        }
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
    except Exception as exc:  # pragma: no cover - 네트워크 의존
        return _error_response(ticker, f"재무 지표 조회 실패: {exc}")

    if not info:
        return _error_response(ticker, "재무 지표 데이터를 찾을 수 없습니다.")
    return {
        "ticker": ticker,
        "success": True,
        "market_cap": info.get("marketCap", "NA"),
        "pe_ratio": info.get("trailingPE", "NA"),
        "dividend_yield": info.get("dividendYield", "NA"),
        "beta": info.get("beta", "NA"),
    }


data_analyst = LlmAgent(
    name="DataAnalyst",
    model=MODEL,
    description="여러 특화 도구로 기초 주식 데이터를 수집·분석하는 데이터 전문가",
    instruction="""
    당신은 3개의 전문 도구로 주식 정보를 수집하는 데이터 애널리스트입니다.
    
    1. **get_company_info(ticker)**: 기업명·산업·섹터 파악
    2. **get_stock_price(ticker, period)**: 현재가와 거래 범위 확보
    3. **get_financial_metrics(ticker)**: 핵심 재무 비율 확인
    
    각 도구가 제공하는 데이터를 명확히 설명하고, 서로 다른 관점을 결합해 정보를 제시하세요.
    """,
    tools=[
        get_company_info,
        get_stock_price,
        get_financial_metrics,
    ],
    output_key="data_analyst_result",
)
