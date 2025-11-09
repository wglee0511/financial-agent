## 환경 설정

1. 가상환경을 생성한 뒤 활성화합니다.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. 필요 라이브러리를 설치합니다.
   ```bash
   pip install -e .
   ```
3. `.env.example`을 참고해 `.env`를 작성하고 필요한 API 키를 채워 넣습니다.

## 폴더 구조

- `financial_advisor/agent.py` : 메인 금융 에이전트 정의 및 하위 도구 연결.
- `financial_advisor/prompt.py` : 금융 자문가 역할을 규정한 한글 프롬프트.
- `financial_advisor/sub_agents/` : 뉴스, 데이터, 재무 애널리스트 하위 에이전트와 도구.
- `tools.py` : Firecrawl 기반 `web_search_tool` 등 보조 도구 정의.
- `pyproject.toml`, `uv.lock` : 패키지 및 의존성 설정.
- `.env`, `.env.example` : 환경 변수 설정 파일.
