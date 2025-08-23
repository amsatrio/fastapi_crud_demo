from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from src.config import environment_config

Base = declarative_base()

DATABASE_URL = environment_config.get_settings().database_url

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session local class
SessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False, # Often set to False for async sessions
    )

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

def create_table_if_not_exist():
    Base.metadata.create_all(bind=engine)
    yield