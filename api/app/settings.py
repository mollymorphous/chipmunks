from enum import StrEnum, auto
from pathlib import Path

import tomllib
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


def load_pyproject_version() -> str | None:
    """Load version number from pyproject.toml"""

    path = Path(__file__).parents[1] / "pyproject.toml"
    if path.exists():
        with path.open("rb") as file:
            project = tomllib.load(file)["project"]
            if project is not None:
                return project["version"]

    return None


class BuildSettings(BaseModel):
    """Information about where this deployment was built from."""

    version: str = Field(default_factory=load_pyproject_version)


class DebugSettings(BaseModel):
    """Debugging settings for use in development."""

    stack_traces: bool = Field(False)
    """Expose stack traces to the client for exceptions resulting in 500 errors."""


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


class LogSettings(BaseModel):
    """Settings for the logging module, including log level and a format string."""

    level: LogLevel = Field(LogLevel.WARNING)
    format: str = Field("[{levelname}] {message} ({filename}:{lineno})")


class Settings(BaseSettings):
    """
    App-wide settings, loaded from `settings.toml` in the working directory, environment variables,
    `.env` files, and Docker secrets.
    """

    build: BuildSettings = Field(default_factory=BuildSettings)
    debug: DebugSettings = Field(DebugSettings())
    log: LogSettings = Field(LogSettings())

    model_config = SettingsConfigDict(
        env_prefix="CHIPMUNKS_",
        env_nested_delimiter="_",
        env_nested_max_split=1,
        toml_file="settings.toml",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


# For development and debugging, you can execute `python app/settings.py` to see resolved settings
if __name__ == "__main__":
    print(Settings().model_dump_json(indent=2))
