from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityOutput(BaseModel):
    name: str
    city: str
    sport_type: str
    picture_urls: list[str]
    elapsed_time_in_seconds: int
    start_datetime: datetime

    polyline: Optional[str]
    distance_in_meters: Optional[int]
    total_elevation_gain_in_meters: Optional[int]
