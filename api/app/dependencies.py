from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine as _AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession as _AsyncSession

logger = getLogger(__name__)


def async_engine(request: Request) -> _AsyncEngine:
    if request.state.sqlalchemy_async_engine is None:
        logger.error("Database not configured, unable to summon SQLAlchemy engine")
        raise HTTPException(503, "Database Unavailable")
    return request.state.sqlalchemy_async_engine


AsyncEngine = Annotated[_AsyncEngine, Depends(async_engine)]


async def async_session(engine: AsyncEngine):
    async with _AsyncSession(engine) as session:
        try:
            yield session
        except OperationalError as error:
            logger.error(error)
            raise HTTPException(503, "Database Unavailable")


AsyncSession = Annotated[_AsyncSession, Depends(async_session)]
