from pydantic import AnyHttpUrl, BaseSettings, SecretStr


class Settings(BaseSettings):
    url: AnyHttpUrl
    api_key: SecretStr

    default_timeout: int = 30

    class Config:
        env_prefix = "PARBLE_"
        env_file_encoding = "utf-8"


__all__ = ("Settings",)
