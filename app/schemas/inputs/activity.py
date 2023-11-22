from pydantic import BaseModel


class GetCurrentActivityInput(BaseModel):
    refresh: bool = False
