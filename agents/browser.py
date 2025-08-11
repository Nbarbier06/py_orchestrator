"""Helpers for downloading web pages and extracting readable content."""

import httpx, re, logging
from bs4 import BeautifulSoup
import trafilatura
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), reraise=True)
async def fetch_html(url: str) -> str:
    """Retrieve raw HTML for a given URL.

    Args:
        url: The web page to fetch.

    Returns:
        The page content as text.
    """

    async with httpx.AsyncClient(timeout=30, headers=HEADERS, follow_redirects=True) as cx:
        r = await cx.get(url)
        r.raise_for_status()
        logger.debug("fetched %s", url)
        return r.text

def extract_readable(html: str, url: str) -> dict[str, str]:
    """Extract a readable document from HTML content.

    Attempts to use *trafilatura* and falls back to BeautifulSoup if needed.

    Args:
        html: Raw HTML markup.
        url: Source URL of the document.

    Returns:
        A dictionary containing ``title``, ``url`` and ``text`` keys.
    """

    # trafilatura peut retourner None -> fallback BS4
    text = trafilatura.extract(html, url=url, include_tables=True, no_fallback=True)
    if not text:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n")
    title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    return {
        "title": (title.group(1).strip() if title else url),
        "url": url,
        "text": text[:20000]
    }
