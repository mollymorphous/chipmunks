"""Database utilities and configuration"""

import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL, make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel


def with_async_driver(url: URL) -> URL:
    """Returns a copy of the URL with appropriate async driver for database."""
    if url.drivername == "postgresql":
        return url.set(drivername="postgresql+asyncpg")
    elif url.drivername == "sqlite":
        return url.set(drivername="postgresql+asyncpg")
    return url


def environment_url() -> URL:
    """
    Get database URL from environment variable CHIPMUNKS_DB_URL.

    If set, environment variables CHIPMUNKS_DB_PASSWORD and CHIPMUNKS_DB_PASSWORD_FILE overrides
    the password present in the URL. CHIPMUNKS_DB_PASSWORD takes precedence
    """
    url = with_async_driver(make_url(os.environ["CHIPMUNKS_DB_URL"]))

    password = os.getenv("CHIPMUNKS_DB_PASSWORD")
    password_file = os.getenv("CHIPMUNKS_DB_PASSWORD_FILE")

    if password is not None:
        return url.set(password=password)
    elif password_file is not None:
        with open(password_file, "rb") as file:
            return url.set(password=file.read())

    return url


async def create_tables():
    """Create SQLModel tables"""
    async with DB_ENGINE.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Create an async SQLAlchemy engine as a global. Enable echo in development.
DB_ENGINE = create_async_engine(environment_url())


def async_session():
    """Create an AsyncSession against the global DB_ENGINE"""
    return AsyncSession(DB_ENGINE)


DbSession = Annotated[AsyncSession, Depends(async_session)]
