# py_orchestrator

Minimal Python orchestrator for [Open WebUI](https://github.com/open-webui). It exposes a
FastAPI service able to plan web searches, retrieve pages and synthesise an answer using
local LLMs served by [Ollama](https://ollama.ai/).

## Configuration

Settings are loaded from environment variables using `pydantic-settings`. The most
relevant options are:

| Variable | Description | Default |
| --- | --- | --- |
| `DEFAULT_SMALL_MODEL` | Model used for lightweight tasks | `qwen2.5:7b` |
| `DEFAULT_BIG_MODEL` | Model used for heavier tasks | `gpt-oss:20b` |
| `NAS_OLLAMA` | Base URL of the NAS Ollama instance | `http://localhost:11434` |
| `LAPTOP_OLLAMA` | Base URL of the laptop Ollama instance | `http://192.168.1.20:11434` |
| `FETCH_CONCURRENCY` | Max concurrent page fetches | `5` |

## Development

Install dependencies and run the API:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Run tests (none are present yet but the command validates the environment):

```bash
pytest
```

## Endpoints

* `GET /health` – basic health check.
* `POST /ask` – accepts an `AskRequest` and returns a synthesised answer.
