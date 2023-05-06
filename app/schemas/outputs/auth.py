from pydantic import BaseModel


class StravaLoginOutput(BaseModel):
    class Athlete(BaseModel):
        class Config:
            orm_mode = True

        uuid: str
        first_name: str
        last_name: str
        picture_url: str

    athlete: Athlete
