from enum import Enum

from pydantic import BaseModel, Field


class StravaWebhookObjectType(str, Enum):
    ACTIVITY = "activity"
    ATHLETE = "athlete"


class StravaWebhookAspectType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class StravaWebhookValidationInput(BaseModel):
    verify_token: str = Field(alias="hub.verify_token")
    challenge: str = Field(alias="hub.challenge")


class StravaWebhookInput(BaseModel):
    object_type: StravaWebhookObjectType
    aspect_type: StravaWebhookAspectType

    object_id: int
    owner_id: int
    subscription_id: int

    event_time: int
    updates: dict

    @property
    def is_create_activity(self) -> bool:
        return (
            self.object_type == StravaWebhookObjectType.ACTIVITY
            and self.aspect_type == StravaWebhookAspectType.CREATE
        )

    @property
    def is_update_activity(self) -> bool:
        return (
            self.object_type == StravaWebhookObjectType.ACTIVITY
            and self.aspect_type == StravaWebhookAspectType.UPDATE
        )
