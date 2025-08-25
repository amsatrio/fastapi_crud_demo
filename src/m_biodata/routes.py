from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import desc, func
from src.dto.page_response import PageResponse
from src.dto.pagination.filtering import Filtering
from src.dto.pagination.sorting import Sorting
from src.m_biodata.schemas import (
    MBiodata,
    MBiodataResponse,
    MBiodataCreate,
    MBiodataUpdate,
)
from src.m_biodata import services
from src.dto.response import AppResponse
from src.config.database_config import get_db
from src.util import file_util
from src.util.file_util import read_file, write_file

import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

log = logging.getLogger(__name__)
m_biodata_router = APIRouter()


# Create a new biodata
@m_biodata_router.post("/", response_model=AppResponse[MBiodataResponse], status_code=201)
async def create_biodata(biodata: MBiodataCreate, db: AsyncSession = Depends(get_db)):
    new_biodata = await services.create(biodata, db)

    response_data = AppResponse[MBiodataResponse](
        status=201,
        message="Success",
        data=new_biodata,
    )
    return response_data


# Get page biodata
@m_biodata_router.get("/pagination", response_model=AppResponse[PageResponse[MBiodataResponse]], status_code=200)
async def read_pagination_biodata(
    page: int = 0, size: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MBiodata).offset(page * size).limit(size))
    biodatas = result.scalars().all()
    
    result_total_data = await db.execute(select(func.count()).select_from(MBiodata))
    total_data = result_total_data.scalar()
    total_pages = int(total_data / size)
    if total_data % size != 0:
        total_pages = total_pages + 1

    biodata_response_list = []
    for biodata in biodatas:
        if biodata.image_path is not None:
            biodata.image = read_file(biodata.image_path)
        biodata_response_list.append(MBiodataResponse.model_validate(biodata))

    page_response = PageResponse[MBiodataResponse] (
        totalPages=total_pages,
        totalElements=total_data,
        content=biodata_response_list
    )

    response_data = AppResponse[PageResponse[MBiodataResponse]](
        status=200,
        message="Success",
        data=page_response,
    )
    return response_data

# POST page biodata
@m_biodata_router.post("/pagination", response_model=AppResponse[PageResponse[MBiodataResponse]], status_code=200)
async def read_pagination_biodata(
    page: int = 0, size: int = 10, sorts: list[Sorting] = [], filters: list[Filtering] = [], db: AsyncSession = Depends(get_db)
):
    # Create the base select statement
    statement = select(MBiodata)
    statement_count = select(func.count()).select_from(MBiodata)

    # Apply filtering
    if len(filters) > 0:
        for filter in filters:
            statement.where(filter.id == filter.value)
            statement_count.where(filter.id == filter.value) 

    # Apply sorting
    if len(sorts) > 0:  
        sort = sorts[0]
        if sort.desc:
            statement = statement.order_by(desc(sort.id))
        else:
            statement = statement.order_by(sort.id)
            
    # Apply pagination
    statement = statement.offset(page * size).limit(size)

    try:
        result = await db.execute(statement)
        result_total_data = await db.execute(statement_count)
    finally:
        await db.close()
        
    
    biodatas = result.scalars().all()
    
    total_data = result_total_data.scalar()
    total_pages = int(total_data / size)
    if total_data % size != 0:
        total_pages = total_pages + 1

    biodata_response_list = []
    for biodata in biodatas:
        if biodata.image_path is not None:
            biodata.image = read_file(biodata.image_path)
        biodata_response_list.append(MBiodataResponse.model_validate(biodata))

    page_response = PageResponse[MBiodataResponse] (
        totalPages=total_pages,
        totalElements=total_data,
        content=biodata_response_list
    )

    response_data = AppResponse[PageResponse[MBiodataResponse]](
        status=200,
        message="Success",
        data=page_response,
    )
    return response_data


# Get all biodata
@m_biodata_router.get("/list", response_model=AppResponse[list[MBiodataResponse]], status_code=200)
async def read_list_biodata(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(MBiodata))
    finally:
        await db.close()
    biodatas = result.scalars().all()
    
    biodata_response_list = []
    for biodata in biodatas:
        if biodata.image_path is not None:
            biodata.image = read_file(biodata.image_path)
        biodata_response_list.append(biodata)

    response_data = AppResponse[list[MBiodataResponse]](
        status=200,
        message="Success",
        data=biodata_response_list,
    )
    return response_data


# Get biodata by ID
@m_biodata_router.get("/{biodata_id}", response_model=AppResponse[MBiodataResponse])
async def read_biodata(biodata_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()
    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")
    
    if existing_biodata.image_path is not None:
        existing_biodata.image = read_file(existing_biodata.image_path)

    log.info("read file success")
    data = MBiodataResponse.model_validate(existing_biodata)
    log.info("model_validate success")
    response_data = AppResponse[MBiodataResponse](
        status=200,
        message="Success",
        data=data,
    )
    return response_data


# Update biodata by ID
@m_biodata_router.put("/{biodata_id}", response_model=AppResponse[MBiodataResponse])
async def update_biodata(
    biodata_id: int, biodata: MBiodataUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()

    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    for key, value in biodata.model_dump(exclude_unset=True).items():
        setattr(existing_biodata, key, value)

    existing_biodata.modified_on = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(existing_biodata)

    response_data = AppResponse[MBiodataResponse](
        status=200,
        message="Success",
        data=existing_biodata,
    )
    return response_data


# Delete biodata by ID
@m_biodata_router.delete("/{biodata_id}", response_model=AppResponse[str])
async def delete_biodata(biodata_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()

    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    await db.delete(existing_biodata)
    await db.commit()
    file_util.delete_file(existing_biodata.image_path)

    response_data = AppResponse[str](status=200, message="Success", data=None)
    return response_data

# Update image biodata
image_base_path = './data'
@m_biodata_router.post("/image/{biodata_id}")
async def update_image_biodata(
    image: Annotated[UploadFile, File()],
    biodata_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MBiodata).where(MBiodata.id == biodata_id))
    existing_biodata = result.scalar_one_or_none()

    if not existing_biodata:
        raise HTTPException(status_code=404, detail="Biodata not found")

    file_path = write_file(image.file, image_base_path, biodata_id, "image", image.filename)

    existing_biodata.modified_on = datetime.now(timezone.utc)
    existing_biodata.image_path = file_path
    # existing_biodata.image = read_file(existing_biodata.image_path)

    await db.commit()
    await db.refresh(existing_biodata)

    response_data = AppResponse[MBiodataResponse](
        status=200,
        message="Success",
        data=existing_biodata,
    )
    return response_data