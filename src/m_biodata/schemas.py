from pydantic import BaseModel, StringConstraints, constr, Field, field_serializer
from typing import Annotated, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, BLOB
import json
from src.config.database_config import Base


class MBiodata(Base):
    __tablename__ = "m_biodata"
    id = Column(BigInteger, primary_key=True, index=True)
    fullname = Column(String(255), nullable=False)
    mobile_phone = Column(String(15), nullable=False)
    image = Column(BLOB, nullable=True)
    image_path = Column(String(255), nullable=True)
    created_by = Column(BigInteger, nullable=True)
    created_on = Column(DateTime, nullable=True)
    modified_by = Column(BigInteger, nullable=True)
    modified_on = Column(DateTime, nullable=True)
    is_delete = Column(Boolean, default=False)
    class Config:
        from_attributes = True
        validate_default = True
        arbitrary_types_allowed = True


class MBiodataCreate(BaseModel):
    fullname: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    mobile_phone: Annotated[str, StringConstraints(min_length=10, max_length=15, pattern=r"^\d{10,15}$")]

class MBiodataUpdate(BaseModel):
    fullname: Optional[Annotated[str, StringConstraints(min_length=1, max_length=255)]] = None
    mobile_phone: Optional[Annotated[str, StringConstraints(min_length=10, max_length=15, pattern=r"^\d{10,15}$")]] = None
    image_path: Optional[str] = None
    image: Optional[bytes] = None

class MBiodataResponse(MBiodataCreate):
    id: int
    created_on: datetime
    modified_on: Optional[datetime] = None
    is_delete: Optional[bool] = False
    image: Optional[bytes] = None

    class Config:
        from_attributes = True
        datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        arbitrary_types_allowed = True
        
    @field_serializer("created_on", "modified_on")
    def serialize_datetime(self, dt: datetime) -> str:
        """Serializes datetime objects to a specific string format."""
        if dt is not None:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return None