from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime
from fastapi.responses import JSONResponse

T = TypeVar("T")
class AppResponse(BaseModel, Generic[T]):
    status: int
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message: str
    data: Optional[T]

    class Config:
        # Ensure datetime is formatted correctly in the JSON output
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
    def generate_json_response(self):
        return JSONResponse(
            status_code=self.status,
            content=self.dict(exclude_none=True),
        )