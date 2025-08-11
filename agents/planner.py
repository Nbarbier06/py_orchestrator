"""Planning agent for building URL lists with language model assistance."""

from config import settings
from services.ollama_client import generate

# model used for small planning tasks
DEFAULT_SMALL = settings.default_small_model

PROFILES = {
    "quick":    {"max_urls": 4,  "task_tokens": 800,  "synth_tokens": 800},
    "balanced": {"max_urls": 8,  "task_tokens": 1500, "synth_tokens": 1500},
    "deep":     {"max_urls": 15, "task_tokens": 2500, "synth_tokens": 2500},
}

async def plan_urls(query: str, mode: str) -> tuple[list[str], dict[str, int]]:
    """Generate a list of relevant URLs for the given query.

    Uses a small model to propose candidate URLs, then deduplicates and clamps
    the results based on a profile selected by *mode*.

    Args:
        query: The user's search query.
        mode: Name of the profile to use when planning.

    Returns:
        A tuple containing the final list of URLs and the profile configuration
        that was applied.
    """

    P = PROFILES.get(mode, PROFILES["balanced"])
    prompt = (
        "Liste 20 URLs pertinentes et récentes pour répondre à la question ci-dessous. "
        "Donne UNIQUEMENT une URL par ligne, sans puce ni texte supplémentaire.\n\n"
        f"Question: {query}"
    )
    seed = await generate(prompt, model=DEFAULT_SMALL, task_tokens=P["task_tokens"])
    urls = [u.strip() for u in seed.splitlines() if u.strip().startswith("http")]
    # dédup + clamp
    final, seen = [], set()
    for u in urls:
        if u not in seen:
            final.append(u)
            seen.add(u)
        if len(final) >= P["max_urls"]:
            break
    return final, P
