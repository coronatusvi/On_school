from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Lớp cấu hình ứng dụng sử dụng OOP
    Kế thừa từ BaseSettings để tự động load từ environment variables
    """
    
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production-at-least-32-characters-long"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "FastAPI OOP Practice"
    debug: bool = True
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"


# Singleton pattern - một instance duy nhất của settings
settings = Settings()
