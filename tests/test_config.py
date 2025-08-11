from config import Settings


def test_env_override(monkeypatch):
    monkeypatch.setenv("DEFAULT_SMALL_MODEL", "unit-model")
    s = Settings()
    assert s.default_small_model == "unit-model"
