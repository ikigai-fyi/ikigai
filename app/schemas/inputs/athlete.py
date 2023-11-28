from pydantic import BaseModel, EmailStr


class PatchAthleteInput(BaseModel):
    email: EmailStr
