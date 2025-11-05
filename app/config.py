from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict( # ✅ Use model_config for BaseModel
        extra='forbid',
        frozen=True,
        str_strip_whitespace=True,
        env_file = ".env"
    )

settings = Settings()