import asyncio
from agents import planner


def test_plan_urls_dedup(monkeypatch):
    async def fake_generate(prompt, model, task_tokens):
        return "http://a.com\nhttp://b.com\nhttp://a.com\nnoturl"
    monkeypatch.setattr(planner, "generate", fake_generate)
    urls, profile = asyncio.run(planner.plan_urls("query", "quick"))
    assert urls == ["http://a.com", "http://b.com"]
    assert profile == planner.PROFILES["quick"]
