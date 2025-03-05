from __future__ import annotations

from enum import StrEnum, auto

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    """Log levels matched to the logging module's standard log level names"""

    @staticmethod
    def _generate_next_value_(name, *args):
        """Keep names uppercase to match what the logging module expects"""
        return name.upper()

    CRITICAL = auto()
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    DEBUG = auto()


class LogConfig(BaseModel):
    level: LogLevel = Field(LogLevel.WARNING)


class DebugConfig(BaseModel):
    stack_traces: bool = Field(False)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CHIPMUNKS_", env_nested_delimiter="_", env_nested_max_split=1
    )

    log: LogConfig = Field(LogConfig())
    debug: DebugConfig = Field(DebugConfig())


if __name__ == "__main__":
    print(Config().model_dump())
