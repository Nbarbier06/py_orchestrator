"""Tools for generating final synthesis from collected documents."""

from config import settings
from services.ollama_client import generate

DEFAULT_BIG = settings.default_big_model
DEFAULT_SMALL = settings.default_small_model

async def synthesize(query: str, docs: list[dict[str, str]], task_tokens: int) -> str:
    """Produce a structured summary from source documents.

    Args:
        query: The original user question.
        docs: A list of documents with ``title``, ``url`` and ``text`` fields.
        task_tokens: Token budget for the synthesis step.

    Returns:
        The generated synthesis text.
    """

    corpus = "\n\n".join([f"### {d['title']}\nURL: {d['url']}\n{d['text']}" for d in docs])
    prompt = (
        "Tu es un assistant de recherche. Fournis une synthèse structurée, précise et neutre. "
        "Ajoute une section 'Sources' listant les URLs utilisées.\n\n"
        f"Question: {query}\n\nDocuments:\n{corpus[:120000]}"
    )
    model = DEFAULT_BIG if task_tokens > 1200 else DEFAULT_SMALL
    return await generate(prompt, model=model, task_tokens=task_tokens)
