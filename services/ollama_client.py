"""Client utilities for interacting with local and remote Ollama instances."""

import httpx, logging
from tenacity import retry, stop_after_attempt, wait_exponential
from config import settings

logger = logging.getLogger(__name__)

NAS_OLLAMA = settings.nas_ollama
LAPTOP_OLLAMA = settings.laptop_ollama

def _pick(task_tokens: int) -> str:
    """Select the Ollama base URL based on the token budget.

    Args:
        task_tokens: Number of tokens requested for the task.

    Returns:
        The base URL of the chosen Ollama instance.
    """

    return LAPTOP_OLLAMA if task_tokens > 1200 else NAS_OLLAMA

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def generate(prompt: str, model: str, task_tokens: int = 800) -> str:
    """Send a prompt to an Ollama model and return the generated response.

    Args:
        prompt: Text prompt to send to the model.
        model: Name of the model to query.
        task_tokens: Token budget, used to pick the server and context window.

    Returns:
        The text produced by the model.
    """

    base = _pick(task_tokens)
    payload = {"model": model, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=120) as cx:
        r = await cx.post(f"{base}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()
        logger.debug("ollama responded in %s", base)
        return data.get("response", "")
