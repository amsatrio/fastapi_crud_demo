

from pydantic import BaseModel


class Sorting(BaseModel):
    id: str
    desc: bool