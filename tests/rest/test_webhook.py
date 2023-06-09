import faker

from tests.factory.strava_webhook import (
    StravaWebhookInputFactory,
    StravaWebhookAspectType,
    StravaWebhookObjectType,
)

fake = faker.Faker()


def test_webhook_validation_unauthorized(client, app):
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={fake.pystr()}&hub.challenge=challenge&hub.mode=subscribe"
    )
    assert response.status_code == 401


def test_webhook_validation_ok(client, app):
    challenge = fake.pystr()
    token = app.config["STRAVA_WEBHOOK_VALIDATION_TOKEN"]
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={token}&hub.challenge={challenge}&hub.mode=subscribe"
    )

    assert response.status_code == 200
    assert response.json == {"hub.challenge": challenge}


def test_webhook_unauthorized(client, app):
    webhook_input = StravaWebhookInputFactory(
        object_type=StravaWebhookObjectType.ACTIVITY,
        aspect_type=StravaWebhookAspectType.CREATE,
        subscription_id=app.config["STRAVA_WEBHOOK_SUBSCRIPTION_ID"] + 1,
    )
    response = client.post("/rest/webhooks/strava", json=webhook_input.dict())
    assert response.status_code == 401


def test_webhook_create_activity(client, app):
    webhook_input = StravaWebhookInputFactory(
        object_type=StravaWebhookObjectType.ACTIVITY,
        aspect_type=StravaWebhookAspectType.CREATE,
        subscription_id=1,
    )
    response = client.post("/rest/webhooks/strava", json=webhook_input.dict())
    assert response.status_code == 200
