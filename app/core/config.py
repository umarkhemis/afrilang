"""
Application settings loaded from environment variables or .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Hugging Face Inference API token
    huggingface_api_key: str = ""

    # Sunbird Sunflower API key (TODO: obtain from Sunbird partnership)
    sunbird_api_key: str = ""

    # Base URL for the AfriLang API (used in SDK / docs)
    base_url: str = "http://localhost:8000"

    # Default fallback model when no registry entry matches the language pair
    default_model_id: str = "facebook/nllb-200-distilled-600M"


settings = Settings()
