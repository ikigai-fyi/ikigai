from pydantic import BaseModel, root_validator
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
    strava_id: str

    polyline: str | None
    distance_in_meters: int | None
    total_elevation_gain_in_meters: int | None

    # Deprecated, remove once app ready
    picture_urls: list[str] | None

    @root_validator
    def fill_picture_urls(cls, values) -> dict:
        values["picture_urls"] = [values["picture_url"]]
        return values
