# Py Orchestrator

Orchestrateur Python minimaliste pour interroger un LLM via Open-WebUI.  
Le service planifie des URLs, extrait leur contenu et synthétise une réponse argumentée.

## Sommaire
1. [Fonctionnalités](#fonctionnalités)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Variables d'environnement](#variables-denvironnement)
6. [API](#api)
7. [Licence](#licence)

## Fonctionnalités
- Planification d’URLs pertinentes via un modèle léger.
- Téléchargement et extraction de texte lisible (Trafilatura/BeautifulSoup).
- Synthèse multi‑documents par un modèle plus grand.
- API FastAPI prête pour intégration avec Open-WebUI.

## Architecture
```
app.py                 # Entrée FastAPI
agents/
  planner.py           # Génère la liste d’URLs
  browser.py           # Télécharge et nettoie les pages
  synth.py             # Produit la synthèse finale
services/
  ollama_client.py     # Client HTTP pour Ollama (réessais + sélection d’hôte)
schemas/
  ask.py               # Modèles Pydantic de requête/réponse
utils/
  logging.py           # Configuration du logging
```

## Installation

### Prérequis
- Python 3.11+
- [Ollama](https://github.com/ollama/ollama) ou service compatible
- `pip`, `git`

### Installation locale
```bash
git clone https://github.com/.../py_orchestrator.git
cd py_orchestrator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8088
```

### Via Docker
```bash
docker build -t py_orchestrator .
docker run -p 8088:8088 \
  -e NAS_OLLAMA=http://nas:11434 \
  -e LAPTOP_OLLAMA=http://laptop:11434 \
  py_orchestrator
```

## Utilisation

### Endpoint `/health`
```bash
curl http://localhost:8088/health
# {"ok": true}
```

### Endpoint `/ask`
```bash
curl -X POST http://localhost:8088/ask -H "Content-Type: application/json" -d '{
  "query": "Quel est l'état actuel de la fusion froide ?",
  "mode": "balanced",
  "override_urls": ["https://example.org/article"]
}'
```
Réponse (exemple) :
```json
{
  "answer": "…",
  "sources": [
    "https://example.org/article",
    "https://..."
  ]
}
```

## Variables d'environnement
| Variable | Description | Valeur par défaut |
|----------|-------------|------------------|
| `NAS_OLLAMA` | URL du serveur Ollama principal | `http://localhost:11434` |
| `LAPTOP_OLLAMA` | URL alternative utilisée pour les tâches volumineuses | `http://192.168.1.20:11434` |
| `DEFAULT_SMALL_MODEL` | Modèle léger pour la planification | `qwen2.5:7b` |
| `DEFAULT_BIG_MODEL` | Modèle plus grand pour la synthèse | `gpt-oss:20b` |

## API
- `GET /health` : test de disponibilité.
- `POST /ask` :
  - **Body** : `{"query": str, "mode": "quick|balanced|deep", "override_urls": [str]}`.
  - **Réponse** : `{"answer": str, "sources": [str]}`.

## Licence
Projet distribué sous licence [MIT](LICENSE).

