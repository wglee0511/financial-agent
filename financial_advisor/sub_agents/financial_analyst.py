import yfinance as yf
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")


def get_income_statement(ticker: str):
    """
    종합적인 매출 및 수익성 분석을 위한 손익계산서를 조회합니다.

    이 도구는 최근 분기와 회계연도에 대한 손익계산서를 불러와 매출, 비용,
    다양한 수준의 이익률 등 기업의 재무 성과를 정밀하게 살펴볼 수 있게 합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - income_statement (str): 다음 항목을 포함한 JSON 문자열
                * 총매출
                * 매출원가
                * 매출총이익
                * 영업비용
                * 영업이익
                * EBITDA
                * 당기순이익
                * 주당순이익(EPS)

    Notes:
        - 일반적으로 최근 4개 분기와 연간 데이터가 제공됩니다.
        - 모든 수치는 기업의 보고 통화 기준입니다.
        - 매출 성장, 마진 추세, 수익성 파악에 유용합니다.

    Example:
        >>> get_income_statement('GOOGL')
        {
            'ticker': 'GOOGL',
            'success': True,
            'income_statement': '{"Total Revenue": {...}, "Net Income": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.income_stmt.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "income_statement": stock.income_stmt.to_json(),
    }


def get_balance_sheet(ticker: str):
    """
    재무 상태와 자본 구조를 파악하기 위한 대차대조표를 조회합니다.

    이 도구는 특정 시점의 자산, 부채, 자본 데이터를 제공해 재무 건전성과
    자본 효율성에 대한 통찰을 제공합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - balance_sheet (str): 다음 항목이 담긴 JSON 문자열
                * 유동자산(현금, 매출채권, 재고)
                * 비유동자산(유형자산, 무형자산, 투자)
                * 유동부채(매입채무, 단기부채)
                * 비유동부채(장기부채, 충당부채 등)
                * 총자본
                * 운전자본 구성

    Notes:
        - 분기/연말 재무 상태의 스냅샷을 제공합니다.
        - 유동비율, 당좌비율 등 유동성 지표 계산에 필수입니다.
        - 부채 수준, 자산 효율, 장부가치 분석에 사용됩니다.
        - 모든 수치는 기업 보고 통화 기준입니다.

    Example:
        >>> get_balance_sheet('AMZN')
        {
            'ticker': 'AMZN',
            'success': True,
            'balance_sheet': '{"Total Assets": {...}, "Total Liabilities": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.balance_sheet.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "balance_sheet": stock.balance_sheet.to_json(),
    }


def get_cash_flow(ticker: str):
    """
    현금 창출 능력과 자본 배분을 평가하기 위한 현금흐름표를 조회합니다.

    이 도구는 영업/투자/재무 활동별 현금 흐름을 상세히 제공하여 기업의
    재무 지속 가능성과 성장 여력을 판단하는 데 도움을 줍니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL')

    Returns:
        dict: 다음 항목을 포함하는 딕셔너리
            - ticker (str): 입력 티커
            - success (bool): 성공 여부
            - cash_flow (str): 다음 항목이 담긴 JSON 문자열
                * 영업활동현금흐름
                * 자본적지출(CapEx)
                * 잉여현금흐름(영업 CF - CapEx)
                * 투자활동현금흐름(인수, 투자 등)
                * 재무활동현금흐름(차입, 배당, 자사주)
                * 현금증감

    Notes:
        - 영업현금흐름은 본업에서 창출되는 현금 규모를 보여줍니다.
        - 잉여현금흐름은 주주 환원·성장 재원 가능성을 나타냅니다.
        - 투자활동 현금흐름이 마이너스면 성장 투자 중일 가능성이 큽니다.
        - 재무활동 현금흐름은 자본 구조 의사결정을 파악하게 합니다.
        - 배당 지속 가능성과 성장 투자 여력을 평가할 때 핵심입니다.

    Example:
        >>> get_cash_flow('META')
        {
            'ticker': 'META',
            'success': True,
            'cash_flow': '{"Operating Cash Flow": {...}, "Free Cash Flow": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.balance_sheet.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "cash_flow": stock.cash_flow.to_json(),
    }


financial_analyst = Agent(
    name="FinancialAnalyst",
    model=MODEL,
    description="손익·재무상태·현금흐름표를 종합 분석하는 재무 전문가",
    instruction="""
    당신은 재무제표를 심층 분석하는 재무 애널리스트입니다. 수행할 일:
    
    1. **손익 분석**: get_income_statement()으로 매출, 수익성, 마진을 파악합니다.
    2. **재무상태 분석**: get_balance_sheet()으로 자산·부채·자본 구조를 점검합니다.
    3. **현금흐름 분석**: get_cash_flow()으로 현금 창출과 자본 배분을 평가합니다.
    
    **사용 가능한 재무 도구**
    - **get_income_statement(ticker)**: 매출·마진·수익성 확인
    - **get_balance_sheet(ticker)**: 자산/부채/자본 및 재무 건전성 확인
    - **get_cash_flow(ticker)**: 영업/잉여 현금흐름과 CapEx 추적
    
    포괄적인 재무제표 데이터를 활용해 기업의 재무 건전성과 성과를 분석하십시오.
    핵심 재무 비율, 추세, 지표에 집중해 기업의 체력과 리스크를 드러내세요.
    """,
    tools=[
        get_income_statement,
        get_balance_sheet,
        get_cash_flow,
    ],
    output_key="financial_analyst_result",
)
