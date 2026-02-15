from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""
    
    # HuggingFace API
    HF_TOKEN: str
    MODEL_NAME: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./jobs.db"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()