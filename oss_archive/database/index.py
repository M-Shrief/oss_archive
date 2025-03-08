from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import URL , create_engine
from sqlalchemy.orm import Session, sessionmaker
#####
from oss_archive.config import DB
from oss_archive.database.models import Base
from oss_archive.seeders.index import seed

db_url = URL.create(
    drivername="postgresql+psycopg",
    username=DB.get('user'),
    password=DB.get('password'),
    host=DB['host'],
    database=DB.get('name'),
    port=DB.get('port')
)


engine = create_async_engine(db_url)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


sync_engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


# Dependency
def get_sync_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield