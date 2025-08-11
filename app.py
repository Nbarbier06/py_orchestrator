import asyncio
import logging
from fastapi import FastAPI
from utils.logging import setup_logging
from schemas.ask import AskRequest, AskResponse
from agents.planner import plan_urls, PROFILES
from agents.browser import fetch_html, extract_readable
from agents.synth import synthesize
from config import settings

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI(title="AI Orchestrator", version="0.1.0")

@app.get("/health")
def health(): return {"ok": True}

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    urls, P = await plan_urls(req.query, req.mode)
    if req.override_urls:
        urls = list(dict.fromkeys(req.override_urls + urls))[:P["max_urls"]]

    sem = asyncio.Semaphore(settings.fetch_concurrency)

    async def gather_page(u: str):
        async with sem:
            try:
                html = await fetch_html(u)
                return extract_readable(html, u)
            except Exception as exc:
                logger.warning("failed to fetch %s: %s", u, exc)
                return None

    results = await asyncio.gather(*(gather_page(u) for u in urls))
    pages = [r for r in results if r]

    answer = await synthesize(req.query, pages, P["synth_tokens"])
    return AskResponse(answer=answer, sources=[p["url"] for p in pages])
