from fastapi import APIRouter, Depends, HTTPException
from src.m_biodata.schemas import (
    MBiodata,
    MBiodataResponse,
    MBiodataCreate,
    MBiodataUpdate,
)
from src.m_biodata import services
from src.dto.response import AppResponse
from src.config.database_config import get_db

from fastapi.responses import JSONResponse
import logging
import time
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

log = logging.getLogger(__name__)
m_biodata_router = APIRouter()


# Create a new biodata
@m_biodata_router.post("/", response_model=AppResponse[MBiodataResponse])
async def create_biodata(biodata: MBiodataCreate, db: AsyncSession = Depends(get_db)):
    new_biodata = await services.create(biodata, db)

    response_data = AppResponse[MBiodataResponse](
        status=201,
        message="Success",
        data=new_biodata,
    )
    return response_data.generate_json_response()


# Get all biodata
@m_biodata_router.get("/list", response_model=AppResponse[list[MBiodataResponse]])
async def read_list_biodata(
    page: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MBiodata).offset(page * limit).limit(limit))
    biodatas = result.scalars().all()

    response_data = AppResponse[list[MBiodataResponse]](
        status=200,
        message="Success",
        data=biodatas,
    )
    return response_data.generate_json_response()


# Get biodata by ID
@m_biodata_router.get("/{biodata_id}", response_model=AppResponse[MBiodataResponse])
async def read_biodata(biodata_id: int, db: AsyncSession = Depends(get_db)):
    # existing_biodata = await services.find_by_id(biodata_id, db)
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()
    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    data = MBiodataResponse.from_orm(existing_biodata)
    response_data = AppResponse[MBiodataResponse](
        status=200,
        message="Success",
        data=data,
    )
    return response_data.generate_json_response()


# Update biodata by ID
@m_biodata_router.put("/{biodata_id}", response_model=AppResponse[MBiodataResponse])
async def update_biodata(
    biodata_id: int, biodata: MBiodataUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()

    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    for key, value in biodata.dict(exclude_unset=True).items():
        setattr(existing_biodata, key, value)

    existing_biodata.modified_on = datetime.utcnow()

    await db.commit()
    await db.refresh(existing_biodata)

    response_data = AppResponse[MBiodataResponse](
        status=200,
        message="Success",
        data=existing_biodata,
    )
    return response_data.generate_json_response()


# Delete biodata by ID
@m_biodata_router.delete("/{biodata_id}", response_model=AppResponse[str])
async def delete_biodata(biodata_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()

    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    await db.delete(existing_biodata)
    await db.commit()

    response_data = AppResponse[str](status=200, message="Success")
    return response_data.generate_json_response()
