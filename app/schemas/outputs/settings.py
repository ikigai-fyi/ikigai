from pydantic import BaseModel, PositiveInt


class SettingsOutput(BaseModel):
    class Config:
        orm_mode = True

    refresh_period_in_hours: PositiveInt
