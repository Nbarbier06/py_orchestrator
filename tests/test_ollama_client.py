from services.ollama_client import _pick, NAS_OLLAMA, LAPTOP_OLLAMA


def test_pick_small():
    assert _pick(800) == NAS_OLLAMA


def test_pick_big():
    assert _pick(1500) == LAPTOP_OLLAMA
