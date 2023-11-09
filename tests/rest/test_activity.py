from http import HTTPStatus

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
        # Deprecated
        "picture_urls": [
            activity.picture_url,
        ],
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
