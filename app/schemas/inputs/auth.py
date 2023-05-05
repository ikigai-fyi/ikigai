from pydantic import BaseModel


class StravaLoginInput(BaseModel):
    code: str
    scope: str
