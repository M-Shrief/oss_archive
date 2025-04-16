from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import URL , create_engine
from sqlalchemy.orm import Session, sessionmaker
#####
from oss_archive.config import DB
# from oss_archive.database.models import Base
from oss_archive.database.models2 import Base

db_url = URL.create(
    drivername="postgresql+psycopg",
    username=DB.get('user'),
    password=DB.get('password'),
    host=DB['host'],
    database=DB.get('name'),
    port=DB.get('port')
)


async_engine = create_async_engine(db_url)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


# Dependency
async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        return db
    finally:
        await db.close()


sync_engine = create_engine(db_url)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


# Dependency
def get_sync_db() -> Session:
    db = SyncSessionLocal()
    try:
        return db
    finally:
        db.close()



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield