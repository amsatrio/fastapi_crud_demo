
from enum import Enum


class FilteringMatchMode(Enum):
	CONTAINS      = "CONTAINS"
	BETWEEN       = "BETWEEN"
	EQUALS        = "EQUALS"
	NOT           = "NOT"
	LESS_THAN     = "LESS_THAN"
	GREATER_THAN  = "GREATER_THAN"