from pathlib import Path
from typing import Annotated

import tomllib
from pydantic import AnyUrl, BaseModel, Field, SecretStr, StringConstraints
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


class BuildConfig(BaseModel):
    version: str = Field(default_factory=load_pyproject_version)
    git_commit: str | None = Field(
        default=None, min_length=40, max_length=40, pattern=r"^[0-9a-f]{40}$"
    )


class DatabaseConfig(BaseModel):
    url: AnyUrl
    password: SecretStr | None = Field(default=None)


class DebugConfig(BaseModel):
    stack_traces: bool = Field(default=False)
    """Expose stack traces to the client: `FastAPI(debug=config.debug.stack_traces)`"""

    echo_sql: bool = Field(default=False)
    """Log SQL to the console: `sqlalchemy.create_engine(echo=config.debug.echo_sql)`"""


class LoggingConfig(BaseModel):
    level: Annotated[str, StringConstraints(to_upper=True)] = Field(default="INFO")
    format: str = Field(default="[%(levelname)s] %(message)s")

    formatters: dict = Field(default={})
    filters: dict = Field(default={})
    handlers: dict = Field(default={})
    loggers: dict = Field(default={})
    root: dict = Field(default={})

    def config_dict(self) -> dict:
        return {
            "version": 1,
            "formatters": {"default": {"format": self.format}} | self.formatters,
            "filters": self.filters,
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                }
            }
            | self.handlers,
            "loggers": self.loggers,
            "root": {"handlers": ["default"], "level": self.level} | self.root,
        }


class Config(BaseSettings):
    """
    App-wide config, loaded from `config.toml` in the working directory, environment
    variables, `.env` files, and Docker secrets.
    """

    build: BuildConfig = Field(default_factory=BuildConfig)
    debug: DebugConfig = Field(default=DebugConfig())
    database: DatabaseConfig | None = Field(default=None)
    logging: LoggingConfig = Field(default=LoggingConfig())

    model_config = SettingsConfigDict(
        env_prefix="CHIPMUNKS_",
        env_nested_delimiter="_",
        env_nested_max_split=1,
        toml_file="config.toml",
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


# For debugging, execute this file to dump the resolved config as JSON
if __name__ == "__main__":
    print(Config().model_dump_json(indent=2))
