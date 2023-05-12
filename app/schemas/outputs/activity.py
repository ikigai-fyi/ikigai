from pydantic import BaseModel
from typing import Optional


class ActivityOutput(BaseModel):
    name: str
    city: str
    sport_type: str
    picture_urls: list[str]
    elapsed_time_in_seconds: int

    polyline: Optional[str]
    distance_in_meters: Optional[int]
    total_elevation_gain_in_meters: Optional[int]
