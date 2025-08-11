import os, asyncio
from fastapi import FastAPI
from utils.logging import setup_logging
from schemas.ask import AskRequest, AskResponse
from agents.planner import plan_urls, PROFILES
from agents.browser import fetch_html, extract_readable
from agents.synth import synthesize

setup_logging()
app = FastAPI(title="AI Orchestrator", version="0.1.0")

@app.get("/health")
def health(): return {"ok": True}

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    urls, P = await plan_urls(req.query, req.mode)
    if req.override_urls:
        urls = list(dict.fromkeys(req.override_urls + urls))[:P["max_urls"]]

    pages: list[dict] = []
    for u in urls:
        try:
            html = await fetch_html(u)
            pages.append(extract_readable(html, u))
        except Exception:
            continue

    answer = await synthesize(req.query, pages, P["synth_tokens"])
    return AskResponse(answer=answer, sources=[p["url"] for p in pages])
