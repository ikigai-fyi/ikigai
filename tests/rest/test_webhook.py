from datetime import datetime
from http import HTTPStatus

import faker
import pytest

from app.models.activity_fetch_job import ActivityFetchJob
from tests.factory.activity import ActivityFactory
from tests.factory.athlete import AthleteFactory
from tests.factory.strava_webhook import (
    StravaWebhookAspectType,
    StravaWebhookInputFactory,
    StravaWebhookObjectType,
)

fake = faker.Faker()


@pytest.mark.usefixtures("app")
def test_webhook_validation_unauthorized(client):
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={fake.pystr()}&hub.challenge=challenge&hub.mode=subscribe",
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_webhook_validation_ok(client, app):
    challenge = fake.pystr()
    token = app.config["STRAVA_WEBHOOK_VALIDATION_TOKEN"]
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={token}&hub.challenge={challenge}&hub.mode=subscribe",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"hub.challenge": challenge}


def test_webhook_unauthorized(client, app):
    webhook_input = StravaWebhookInputFactory(
        object_type=StravaWebhookObjectType.ACTIVITY,
        aspect_type=StravaWebhookAspectType.CREATE,
        subscription_id=app.config["STRAVA_WEBHOOK_SUBSCRIPTION_ID"] + 1,
    )
    response = client.post("/rest/webhooks/strava", json=webhook_input.dict())
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_webhook_create_activity(client, app):
    athlete = AthleteFactory()
    webhook_input = StravaWebhookInputFactory(
        object_type=StravaWebhookObjectType.ACTIVITY,
        aspect_type=StravaWebhookAspectType.CREATE,
        subscription_id=app.config["STRAVA_WEBHOOK_SUBSCRIPTION_ID"],
        owner_id=athlete.strava_id,
        object_id=9024223766,
    )
    response = client.post("/rest/webhooks/strava", json=webhook_input.dict())
    assert response.status_code == HTTPStatus.OK

    job = ActivityFetchJob.query.one()
    assert job.activity_strava_id == webhook_input.object_id
    assert job.athlete_id == athlete.id
    assert job.done_at is None
    assert job.do_after > datetime.utcnow()


def test_webhook_update_activity(client, app):
    athlete = AthleteFactory()
    activity = ActivityFactory(strava_id=9033948628, athlete=athlete, updated_at=None)
    webhook_input = StravaWebhookInputFactory(
        object_type=StravaWebhookObjectType.ACTIVITY,
        aspect_type=StravaWebhookAspectType.UPDATE,
        subscription_id=app.config["STRAVA_WEBHOOK_SUBSCRIPTION_ID"],
        owner_id=athlete.strava_id,
        object_id=activity.strava_id,
    )
    response = client.post("/rest/webhooks/strava", json=webhook_input.dict())
    assert response.status_code == HTTPStatus.OK

    job = ActivityFetchJob.query.one()
    assert job.activity_strava_id == activity.strava_id
    assert job.athlete_id == athlete.id
    assert job.done_at is None
    assert job.do_after < datetime.utcnow()
