from enum import Enum

from pydantic import BaseModel

from .activity import ActivityOutput


class PickType(str, Enum):
    RANDOM = "random"
    X_YEARS_AGO = "x_years_ago"


class ActivityPickOutput(BaseModel):
    activity: ActivityOutput
    pick_type: PickType
