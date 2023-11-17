from datetime import datetime, timedelta
from http import HTTPStatus

import pytest

from tests.factory.activity import ActivityFactory
from tests.factory.athlete import AthleteFactory


def test_get_random_activity(client):
    athlete = AthleteFactory()
    activity = ActivityFactory(athlete=athlete)
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
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
    }


def test_get_random_activity_no_activity_with_picture(client):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "type": "NoRecentActivityWithPictureError",
        "message": "No recent activity has pictures to be dispayed",
    }


def test_get_random_activity_last_active(client):
    athlete = AthleteFactory(last_active_at=None)
    client.authenticated(athlete).get("/rest/activities/random")
    assert athlete.last_active_at is not None


def test_pick_activity_random(client):
    athlete = AthleteFactory()
    activity = ActivityFactory(athlete=athlete)
    response = client.authenticated(athlete).get("/rest/activities/pick")

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
        "pick_type": "random",
    }


@pytest.mark.parametrize("x_years", [1, 2, 5, 10])
def test_pick_activity_x_years_ago(client, x_years):
    athlete = AthleteFactory()

    target_datetime = datetime(
        year=datetime.today().year - x_years,
        month=datetime.today().month,
        day=datetime.today().day,
    )
    activity = ActivityFactory(
        athlete=athlete,
        start_datetime=target_datetime,
    )

    # Noise
    ActivityFactory.create_batch(size=10, athlete=athlete)
    ActivityFactory.create_batch(
        size=10,
        athlete=athlete,
        start_datetime=target_datetime + timedelta(days=1),
    )

    response = client.authenticated(athlete).get("/rest/activities/pick")

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
        "pick_type": "x_years_ago",
    }


def test_pick_activity_last_active(client):
    athlete = AthleteFactory(last_active_at=None)
    client.authenticated(athlete).get("/rest/activities/random")
    assert athlete.last_active_at is not None


def test_current_activity_is_deterministic(client):
    athlete = AthleteFactory()
    ActivityFactory.create_batch(size=100, athlete=athlete)

    distinct_ids = {
        client.authenticated(athlete)
        .get("/rest/activities/current")
        .json["activity"]["strava_id"]
        for _ in range(10)
    }

    assert len(distinct_ids) == 1
