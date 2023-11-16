from datetime import datetime

from pydantic import BaseModel


class ActivityOutput(BaseModel):
    class Config:
        orm_mode = True

    name: str
    has_custom_name: bool
    sport_type: str
    elapsed_time_in_seconds: int
    start_datetime: datetime
    city: str
    picture_url: str
    strava_id: str

    polyline: str | None
    distance_in_meters: int | None
    total_elevation_gain_in_meters: int | None
