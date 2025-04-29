from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseModel):
    debug: bool


class SecurityConfig(BaseModel):
    password_hash_pepper: str
    password_hash_count: int


class DatabaseConfig(BaseModel):
    uri: SecretStr


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    server: ServerConfig
    security: SecurityConfig
    db: DatabaseConfig


def gather_config() -> Config:
    return Config()
