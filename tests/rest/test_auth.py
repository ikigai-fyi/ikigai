import random
from http import HTTPStatus
from unittest.mock import ANY

import pytest

from app.models.activity import Activity
from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete
from tests.fixtures.resources.bike import BIKE_WITH_PICTURES_DETAIL
from tests.fixtures.resources.run import RUN_WITH_PICTURES_DETAIL


@pytest.mark.usefixtures(
    "post_strava_token_response_mock",
    "get_strava_athlete_response_mock",
    "get_activities_response_mock_run_and_bike",
    "get_activity_response_mock_run",
    "get_activity_response_mock_bike",
    "get_reverse_geocoding_mock",
)
def test_strava_login(client):
    random.seed(1)

    response = client.post(
        "/rest/auth/login/strava",
        json={
            "code": "some_code",
            "scope": "activity:read_all,profile:read_all",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "jwt": ANY,
        "athlete": {
            "uuid": ANY,
            "email": None,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "picture_url": "picture_url",
            "city": "Annecy",
        },
    }

    # The two activities have been fetched
    activities = Activity.query.all()
    assert len(activities) == 2  # noqa: PLR2004

    # Run first and bike after
    assert activities[0].strava_id == RUN_WITH_PICTURES_DETAIL["id"]
    assert activities[1].strava_id == BIKE_WITH_PICTURES_DETAIL["id"]

    # Bike was fetched using the queue
    assert ActivityFetchJob.query.count() == 1
    job = ActivityFetchJob.query.one()
    assert job.done_at is not None
    assert job.activity_strava_id == BIKE_WITH_PICTURES_DETAIL["id"]

    athlete = Athlete.query.one()
    assert athlete.created_activities_jobs_at is not None
