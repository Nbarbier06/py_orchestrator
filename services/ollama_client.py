import httpx, logging
from tenacity import retry, stop_after_attempt, wait_exponential
from config import settings

logger = logging.getLogger(__name__)

NAS_OLLAMA = settings.nas_ollama
LAPTOP_OLLAMA = settings.laptop_ollama

def _pick(task_tokens: int) -> str:
    return LAPTOP_OLLAMA if task_tokens > 1200 else NAS_OLLAMA

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def generate(prompt: str, model: str, task_tokens: int = 800) -> str:
    base = _pick(task_tokens)
    payload = {"model": model, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=120) as cx:
        r = await cx.post(f"{base}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()
        logger.debug("ollama responded in %s", base)
        return data.get("response", "")
