import os
from services.ollama_client import generate

DEFAULT_BIG = os.getenv("DEFAULT_BIG_MODEL", "gpt-oss:20b")
DEFAULT_SMALL = os.getenv("DEFAULT_SMALL_MODEL", "qwen2.5:7b")

async def synthesize(query: str, docs: list[dict], task_tokens: int):
    corpus = "\n\n".join([f"### {d['title']}\nURL: {d['url']}\n{d['text']}" for d in docs])
    prompt = (
        "Tu es un assistant de recherche. Fournis une synthèse structurée, précise et neutre. "
        "Ajoute une section 'Sources' listant les URLs utilisées.\n\n"
        f"Question: {query}\n\nDocuments:\n{corpus[:120000]}"
    )
    model = DEFAULT_BIG if task_tokens > 1200 else DEFAULT_SMALL
    return await generate(prompt, model=model, task_tokens=task_tokens)
