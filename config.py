from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    default_small_model: str = "qwen2.5:7b"
    default_big_model: str = "gpt-oss:20b"
    nas_ollama: str = "http://localhost:11434"
    laptop_ollama: str = "http://192.168.1.20:11434"
    fetch_concurrency: int = 5

settings = Settings()
