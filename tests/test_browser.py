from agents import browser


def test_extract_readable_fallback(monkeypatch):
    html = "<html><head><title>Example</title></head><body><p>Hello</p></body></html>"
    monkeypatch.setattr(browser.trafilatura, "extract", lambda html, url, include_tables=True, no_fallback=True: None)
    data = browser.extract_readable(html, "http://example.com")
    assert data["title"] == "Example"
    assert "Hello" in data["text"]
