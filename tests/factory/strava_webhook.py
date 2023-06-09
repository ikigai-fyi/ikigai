import factory

from app.schemas.inputs.webhook import (
    StravaWebhookAspectType,
    StravaWebhookInput,
    StravaWebhookObjectType,
)


class StravaWebhookInputFactory(factory.Factory):
    class Meta:
        model = StravaWebhookInput

    object_type = factory.Faker("random_element", elements=StravaWebhookObjectType)
    aspect_type = factory.Faker("random_element", elements=StravaWebhookAspectType)

    object_id = factory.Faker("pyint")
    owner_id = factory.Faker("pyint")
    subscription_id = factory.Faker("pyint")

    event_time = factory.Faker("pyint")
    updates: dict = {}
