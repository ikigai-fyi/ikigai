from pydantic import BaseModel


class ActivityOutput(BaseModel):
    name: str
    polyline: str
    distance_in_meters: float
    elapsed_time_in_seconds: int
