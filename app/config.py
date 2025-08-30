"""
Cấu hình ứng dụng từ environment variables.
"""
import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Cấu hình ứng dụng."""
    
    # Server config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Ollama config
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TIMEOUT: int = 600
    
    # Agent config
    AGENTS_REPO_URL: str = "https://github.com/contains-studio/agents"
    AGENTS_LOCAL_PATH: str = "./agents_repo"
    
    # Logging
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Cấu hình logging
import logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

# Set specific loggers
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
logging.getLogger("core.ollama_client").setLevel(logging.DEBUG)