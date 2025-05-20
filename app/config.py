from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "YOUR_API_KEY"
    AUTH_TOKEN: str = "YOUR_AUTH_TOKEN"
    DEFAULT_TIMEZONE: float = 2.0
    DEFAULT_PLACE: str = "Zurich, Switzerland"
    DEFAULT_HOUSE_SYSTEM: str = "P"

    class Config:
        env_file = ".env"

settings = Settings()
