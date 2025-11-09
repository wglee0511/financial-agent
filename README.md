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

```
financial-analyst
├── financial_advisor
│   ├── agent.py               # 메인 금융 에이전트 및 도구 연결
│   ├── prompt.py              # 금융 자문 프롬프트(한글)
│   └── sub_agents
│       ├── data_analyst.py    # 기업 정보/주가/재무 지표 수집 도구
│       ├── financial_analyst.py
│       ├── news_analyst.py
│       └── sector_analyst.py  # 섹터별 티커 발굴 에이전트
├── tools.py                   # web_search_tool 등 공용 도구
├── pyproject.toml / uv.lock   # 프로젝트 설정 및 의존성
├── README.md / codex.md       # 문서 및 내부 규칙
└── .env / .env.example        # 환경 변수 정의
```

## 실행 방법

1. 환경 변수 설정과 가상환경 활성화가 완료되었는지 확인합니다.
2. Codex CLI 또는 ADK 실행 환경에서 프로젝트 루트로 이동합니다.
3. 다음 명령으로 에이전트를 실행합니다.
   ```bash
   adk run financial_advisor.agent:root_agent
   ```
   - `adk web` 등을 활용한다면 사전에 `adk` CLI가 설치되어 있어야 합니다.
4. 실행 중 “AI 산업 섹터 전망”과 같이 섹터 기반 요청을 하면 `sector_analyst`가 자동으로 티커를 수집하고 나머지 하위 에이전트가 후속 분석을 수행합니다.
