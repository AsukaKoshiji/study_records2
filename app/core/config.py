from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Record API"
    app_description: str = "学習記録、目標、カレンダー、進捗確認を管理するMVP APIです。"
    app_version: str = "0.1.0"
    database_url: str = "mysql+pymysql://learning_user:learning_password@localhost:3306/learning_records"
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
