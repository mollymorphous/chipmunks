import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import func, select

from .config import Config
from .db import DbSession, create_tables
from .models import Greeting


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables
    yield


app = FastAPI(title="Chipmunks", lifespan=lifespan)


# Set up app instance
config = Config()
logging.basicConfig(level=config.log.level, format=config.log.format, style="{")
app = FastAPI(
    title="Chipmunks",
    debug=config.debug.stack_traces,
    version=config.build.version,
    lifespan=lifespan,
)


@app.get("/")
async def hello(session: DbSession) -> Greeting:
    """Show a random greeting."""
    return await session.scalar(select(Greeting).limit(1).order_by(func.random()))


@app.post("/greetings")
async def create_greeting(greeting: Greeting, session: DbSession) -> Greeting:
    session.add(greeting)
    await session.commit()
    await session.refresh(greeting)
    return greeting


@app.get("/greetings")
async def read_greetings(session: DbSession) -> list[Greeting]:
    return (await session.scalars(select(Greeting))).all()
