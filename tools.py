from typing import Any, Dict, List, Optional

import dotenv

dotenv.load_dotenv()
import re
import os
from firecrawl import FirecrawlApp, ScrapeOptions


def _clean_markdown(text: str) -> str:
    """불필요한 개행·링크를 제거한 요약 텍스트."""
    cleaned = re.sub(r"\\+|\n+", " ", text or "").strip()
    cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)
    return cleaned


def web_search_tool(
    query: Optional[str] = None,
    request: Optional[str] = None,
    **kwargs: Any,
) -> List[Dict[str, Any]]:
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    search_query = query or request or kwargs.get("query") or kwargs.get("q")

    if not search_query:
        return [
            {
                "title": "검색어 오류",
                "url": "",
                "markdown": "검색어(query)가 제공되지 않았습니다.",
            }
        ]

    try:
        response = app.search(
            query=search_query,
            limit=5,
            scrape_options=ScrapeOptions(
                formats=["markdown"],
            ),
        )
    except Exception as exc:  # pragma: no cover - 네트워크 의존
        return [
            {
                "title": "검색 실패",
                "url": "",
                "markdown": f"Firecrawl 검색 실패: {exc}",
            }
        ]

    if not response.success:
        return [
            {
                "title": "검색 실패",
                "url": "",
                "markdown": getattr(response, "error", "검색 응답 실패"),
            }
        ]

    cleaned_chunks: List[Dict[str, Any]] = []

    for result in response.data or []:
        markdown = result.get("markdown") or result.get("content") or ""
        if not markdown:
            continue

        cleaned_result = {
            "title": result.get("title"),
            "url": result.get("url"),
            "markdown": _clean_markdown(markdown),
        }
        cleaned_chunks.append(cleaned_result)

    if not cleaned_chunks:
        return [
            {
                "title": "검색 결과 없음",
                "url": "",
                "markdown": "유의미한 검색 결과를 찾지 못했습니다.",
            }
        ]

    return cleaned_chunks
