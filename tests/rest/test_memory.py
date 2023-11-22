from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time

from tests.factory.activity import ActivityFactory
from tests.factory.athlete import AthleteFactory


def test_get_memory_format(client):
    athlete = AthleteFactory()
    activity = ActivityFactory(athlete=athlete)
    response = client.authenticated(athlete).get("/rest/memories/current")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "activity": {
            "city": activity.city,
            "distance_in_meters": activity.distance_in_meters,
            "elapsed_time_in_seconds": activity.elapsed_time_in_seconds,
            "name": activity.name,
            "has_custom_name": True,
            "picture_url": activity.picture_url,
            "polyline": activity.polyline,
            "sport_type": activity.sport_type,
            "start_datetime": activity.start_datetime.isoformat(),
            "total_elevation_gain_in_meters": activity.total_elevation_gain_in_meters,
            "strava_id": str(activity.strava_id),
        },
        "type": "random",
    }


def test_get_memory_should_be_deterministic(client):
    athlete = AthleteFactory()
    ActivityFactory.create_batch(size=50, athlete=athlete)

    distinct_ids = {
        client.authenticated(athlete)
        .get("/rest/memories/current")
        .json["activity"]["strava_id"]
        for _ in range(10)
    }

    assert len(distinct_ids) == 1


def test_get_memory_should_expire(client):
    initial_date = datetime.utcnow()
    athlete = AthleteFactory(memory_refreshed_at=initial_date)
    ActivityFactory.create_batch(size=50, athlete=athlete)

    first_activity = client.authenticated(athlete).get("/rest/memories/current").json
    second_activity = client.authenticated(athlete).get("/rest/memories/current").json

    with freeze_time(
        athlete.memory_refreshed_at
        + timedelta(hours=athlete.settings.refresh_period_in_hours + 1),
    ):
        third_activity = (
            client.authenticated(athlete).get("/rest/memories/current").json
        )

    assert first_activity == second_activity
    assert second_activity != third_activity
    assert athlete.memory_refreshed_at > initial_date


def test_get_memory_with_force_refresh_should_refresh(client):
    initial_date = datetime.utcnow()
    athlete = AthleteFactory(memory_refreshed_at=initial_date)
    ActivityFactory.create_batch(size=50, athlete=athlete)

    distinct_ids = set()

    for _ in range(10):
        distinct_ids.add(
            client.authenticated(athlete)
            .get("/rest/memories/current?refresh=true")
            .json["activity"]["strava_id"],
        )

    assert len(distinct_ids) > 1
    assert athlete.memory_refreshed_at > initial_date
