from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from src.config import configuration
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = configuration.get_settings().database_url

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


def create_table_if_not_exist():
    Base.metadata.create_all(bind=engine)
    yield