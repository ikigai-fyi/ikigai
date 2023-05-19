from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityOutput(BaseModel):
    name: str
    sport_type: str
    picture_urls: list[str]
    elapsed_time_in_seconds: int
    start_datetime: datetime

    city: Optional[str]
    polyline: Optional[str]
    distance_in_meters: Optional[int]
    total_elevation_gain_in_meters: Optional[int]
