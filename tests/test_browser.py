import asyncio
import httpx
from agents import browser


def test_extract_readable_fallback(monkeypatch):
    html = "<html><head><title>Example</title></head><body><p>Hello</p></body></html>"
    monkeypatch.setattr(browser.trafilatura, "extract", lambda html, url, include_tables=True, no_fallback=True: None)
    data = browser.extract_readable(html, "http://example.com")
    assert data["title"] == "Example"
    assert "Hello" in data["text"]


def test_fetch_html_reuses_client():
    async def handler(request):
        handler.calls += 1
        return httpx.Response(200, text="ok")

    handler.calls = 0
    transport = httpx.MockTransport(handler)

    async def main():
        async with httpx.AsyncClient(transport=transport) as client:
            await browser.fetch_html("http://example.com", client=client)
            await browser.fetch_html("http://example.com", client=client)

    asyncio.run(main())
    assert handler.calls == 2
