from pydantic import BaseModel, Field


class StravaWebhookValidationInput(BaseModel):
    verify_token: str = Field(alias="hub.verify_token")
    challenge: str = Field(alias="hub.challenge")
