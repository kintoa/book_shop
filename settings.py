from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Book Shop"
    items_per_page: int = 10

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()