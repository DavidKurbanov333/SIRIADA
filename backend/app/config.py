from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Существующие настройки
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Настройки внешнего сервера
    EXTERNAL_SERVER_URL: str = "https://kvmnfs-cs2.timeweb.cloud/75f11686-6228-4218-83a8-0458b879985b"
    EXTERNAL_SERVER_API_KEY: str = ""  # Если нужен API ключ
    
    class Config:
        env_file = ".env"

settings = Settings() 