from typing import Any

from pydantic import AnyHttpUrl, BaseSettings, SecretStr, ValidationError

from parble.exceptions import ConfigurationError


class Settings(BaseSettings):
    url: AnyHttpUrl
    api_key: SecretStr

    default_timeout: int = 30

    class Config:
        env_prefix = "PARBLE_"
        env_file_encoding = "utf-8"

    def __init__(self, **values: Any):
        """
        Wrap the pydantic validation error and raise a config error from it
        """
        values = {k: v for k, v in values.items() if v is not None}
        try:
            super().__init__(**values)
        except ValidationError as e:
            msg = f"missing or incorrect settings value for {', '.join([' '.join(x['loc']) for x in e.errors()])}"
            raise ConfigurationError(msg) from e


__all__ = ("Settings",)
