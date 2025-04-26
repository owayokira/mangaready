from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseModel):
    debug: bool


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__')

    server: ServerConfig


def gather_config() -> Config:
    return Config()
