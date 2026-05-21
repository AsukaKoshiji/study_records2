from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user:password@db:3306/learning_record"

    class Config:
        env_file = ".env"


settings = Settings()