from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Any
from sqlalchemy.engine import URL , create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from collections.abc import AsyncGenerator, Generator
#####
from oss_archive.config import DB
from oss_archive.database.models import Base

db_url = URL.create(
    drivername="postgresql+psycopg",
    username=DB.get('user'),
    password=DB.get('password'),
    host=DB['host'],
    database=DB.get('name'),
    port=int(str(DB.get('port')))
)


async_engine: AsyncEngine = create_async_engine(db_url)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

# FastAPI's dependency with yield: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


sync_engine = create_engine(db_url)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# FastAPI's dependency with yield: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_sync_db() -> Generator[Session, Any]:
    db: Session = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield