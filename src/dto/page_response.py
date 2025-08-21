from pydantic import BaseModel
from typing import Generic, TypeVar
from datetime import datetime

T = TypeVar("T")
class PageResponse(BaseModel, Generic[T]):
    totalElements: int
    totalPages: int
    content: list[T]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }
        arbitrary_types_allowed = True