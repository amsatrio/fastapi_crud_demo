from pydantic import BaseModel
from src.dto.pagination.filtering_data_type import FilteringDataType
from src.dto.pagination.filtering_match_mode import FilteringMatchMode
from src.dto.pagination.filtering_mode import FilteringMode

class Filtering(BaseModel):
    id: str
    value: str
    dataType: FilteringDataType
    matchMode: FilteringMatchMode
    mode: FilteringMode