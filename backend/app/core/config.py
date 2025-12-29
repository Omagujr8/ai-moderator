from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV:str

    DATABASE_URL:str

    SECRET_KEY:str
    ALGORITHM:str

    REDIS_URL:str
    API_KEY_HEADER:str

    class Config:
        env_file = ".env"

settings = Settings()