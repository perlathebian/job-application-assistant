from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""
    
    # HuggingFace API
    HF_TOKEN: str
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Groq API
    GROQ_API_KEY: str

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./jobs.db"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()