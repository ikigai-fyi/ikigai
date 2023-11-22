from enum import Enum

from pydantic import BaseModel

from .activity import ActivityOutput


class MemoryType(str, Enum):
    RANDOM = "random"
    X_YEARS_AGO = "x_years_ago"


class MemoryOutput(BaseModel):
    activity: ActivityOutput
    type: MemoryType
