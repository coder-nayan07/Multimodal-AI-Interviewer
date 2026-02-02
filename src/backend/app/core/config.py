import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Centralized Configuration Management.
    Validates that all required Environment Variables exist on startup.
    """
    # --- App Config ---
    PROJECT_NAME: str = "AI Interviewer"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "local"
    
    # --- API Keys (Required) ---
    # Pydantic will auto-read these from your .env file
    GROQ_API_KEY: str
    LLAMA_CLOUD_API_KEY: str
    
    # Optional for now (we will add these later)
    DEEPGRAM_API_KEY: str = "" 
    ELEVENLABS_API_KEY: str = ""

    # --- Pydantic V2 Configuration ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignore extra keys in .env (like comments)
    )

@lru_cache()
def get_settings():
    return Settings()

# Global singleton instance
settings = get_settings()