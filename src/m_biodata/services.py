
from src.m_biodata.schemas import (
    MBiodata,
    MBiodataResponse,
    MBiodataCreate,
    MBiodataUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import time
from datetime import datetime


async def create(biodata: MBiodataCreate, db: AsyncSession) -> MBiodataResponse:
    new_biodata = MBiodata(**biodata.dict(), created_on=datetime.utcnow(), id=int(time.time()))
    db.add(new_biodata)
    await db.commit()
    await db.refresh(new_biodata)

    return new_biodata

async def find_by_id(id: int, db: AsyncSession) -> MBiodataResponse:
    result = await db.execute(select(MBiodata).where(MBiodata.id == id))
    existing_biodata = result.scalar_one_or_none()
    return existing_biodata