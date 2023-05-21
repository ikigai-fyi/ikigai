from pydantic import BaseModel, root_validator
from typing import Optional
from datetime import datetime


class ActivityOutput(BaseModel):
    class Config:
        orm_mode = True

    name: str
    sport_type: str
    elapsed_time_in_seconds: int
    start_datetime: datetime
    city: str
    picture_url: str

    polyline: Optional[str]
    distance_in_meters: Optional[int]
    total_elevation_gain_in_meters: Optional[int]

    # Deprecated, remove once app ready
    picture_urls: Optional[list[str]]

    @root_validator
    def fill_picture_urls(cls, values) -> dict:
        values["picture_urls"] = [values["picture_url"]]
        return values
