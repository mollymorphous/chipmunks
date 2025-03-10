import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from .config import Config

config = Config()
logger = logging.getLogger(__name__)
logging.config.dictConfig(config.logging.config_dict())


@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.database is None:
        logger.warning(
            "Database not configured. You may need to set $CHIPMUNKS_DATABASE_URL."
        )
        engine = None
    else:
        try:
            url = config.database.sqlalchemy_url()
            engine = create_async_engine(url, echo=config.debug.echo_sql)
            logger.debug("Configured database at '%s'", url)
        except Exception as exception:
            logger.critical(exception)
            raise exception

    yield {"sqlalchemy_async_engine": engine}

    if engine is not None:
        await engine.dispose()


app = FastAPI(
    title="Chipmunks",
    lifespan=lifespan,
    debug=config.debug.stack_traces,
    version=config.build.version,
)


@app.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
