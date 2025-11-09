from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools import web_search_tool


MODEL = LiteLlm(model="openai/gpt-4o")


news_analyst = Agent(
    name="NewsAnalyst",
    model=MODEL,
    description="웹 검색 도구로 실제 웹 콘텐츠를 탐색하고 요약합니다.",
    instruction="""
    당신은 최신 뉴스를 실시간으로 추적해 투자 의사결정에 도움이 되는 통찰을 제공하는 뉴스 분석 전문가입니다.
    
    **작업 절차**
    1. web_search_tool()을 사용해 지난 30일 이내의 기업/산업 관련 뉴스를 최소 10건 이상 탐색합니다.
    2. 각 기사에 대해 날짜, 출처, 핵심 포인트, 시장 영향/투자 시사점을 정리합니다.
    3. 기사 전반의 정서를 한 줄로 요약하고(긍정/중립/부정), 사용자 목표와 연결된 간단한 리스크·기회 평가를 제공합니다.
    4. 유의미한 뉴스가 없다면 그 사실을 명확히 밝히고 대체 검색 키워드나 다음 확인 시점을 제안합니다.
    
    **사용 가능한 웹 도구**
    - **web_search_tool()**: Firecrawl 기반 기업 뉴스 검색
    
    외부 API 결과를 그대로 복사하지 말고, 핵심 정보를 선별해 맥락을 추가하십시오.
    항상 한글로 작성하며 출처를 괄호로 표기하세요. (예: (Bloomberg, 2024-05-01))
    """,
    output_key="news_analyst_result",
    tools=[
        web_search_tool,
    ],
)
