import httpx, re
from bs4 import BeautifulSoup
import trafilatura

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=30, headers=HEADERS, follow_redirects=True) as cx:
        r = await cx.get(url)
        r.raise_for_status()
        return r.text

def extract_readable(html: str, url: str) -> dict:
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
