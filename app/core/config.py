from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Record API"
    app_description: str = "API for managing study records"
    app_version: str = "1.0.0"

    mysql_host: str = "db"
    mysql_port: int = 3306
    mysql_database: str = "learning_records"
    mysql_user: str = "learning_user"
    mysql_password: str = "learning_password"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/"
            f"{self.mysql_database}"
        )


settings = Settings()



class Settings(BaseSettings):
    # App
    app_name: str = "Learning Record API"
    app_description: str = "Study record management API"
    app_version: str = "1.0.0"

    # CORS
    cors_origins: list[str] = ["*"]

    # DB
    mysql_host: str = "db"
    mysql_port: int = 3306
    mysql_database: str = "learning_records"
    mysql_user: str = "learning_user"
    mysql_password: str = "learning_password"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/"
            f"{self.mysql_database}"
        )


settings = Settings()