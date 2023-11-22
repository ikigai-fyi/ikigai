from pydantic import BaseModel


class GetCurrentMemoryInput(BaseModel):
    refresh: bool = False
