from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, BLOB
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


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


class MBiodataCreate(BaseModel):
    fullname: constr(min_length=1, max_length=255)
    mobile_phone: constr(min_length=10, max_length=15) = Field(
        ..., pattern=r"^\d{10,15}$"
    )


class MBiodataUpdate(BaseModel):
    fullname: Optional[constr(min_length=1, max_length=255)]
    mobile_phone: Optional[constr(min_length=10, max_length=15)] = Field(
        ..., pattern=r"^\d{10,15}$"
    )
    image_path: Optional[str]
    image: Optional[bytes]


class MBiodataResponse(MBiodataCreate):
    id: int
    created_on: datetime
    modified_on: Optional[datetime]
    is_delete: Optional[bool]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Custom encoder for datetime
        }

    def __init__(
        self,
        id: int,
        created_on: datetime,
        modified_on: Optional[datetime],
        is_delete: Optional[bool],
    ):
        self.id = id
        self.created_on = created_on
        self.modified_on = modified_on
        self.is_delete = is_delete

    def to_json(self):
        return json.dumps(self, default=self.json_serial)

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")
