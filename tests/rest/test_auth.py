from http import HTTPStatus
from unittest.mock import ANY, MagicMock

import pytest

from app.models.activity import Activity
from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete
from tests.fixtures.resources.run import RUN_WITH_PICTURES_PREVIEW


@pytest.mark.usefixtures(
    "post_strava_token_response_mock",
    "get_strava_athlete_response_mock",
    "get_activities_response_mock_run",
    "get_run_activity_response_mock_run",
    "get_reverse_geocoding_mock",
)
def test_strava_login(client, monkeypatch):
    mock_update = MagicMock()
    monkeypatch.setattr(Athlete, "update_created_activities_jobs_at", mock_update)

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
            "first_name": "Firstname",
            "last_name": "Lastname",
            "picture_url": "picture_url",
            "city": "Annecy",
        },
    }

    assert ActivityFetchJob.query.count() == 1
    job = ActivityFetchJob.query.one()
    assert job.done_at is not None
    assert job.activity_strava_id == RUN_WITH_PICTURES_PREVIEW["id"]

    assert Activity.query.count() == 1
    activity = Activity.query.one()
    assert activity.strava_id == RUN_WITH_PICTURES_PREVIEW["id"]

    # FIXME: athlete is created in the endpoint but field update in the task
    # It seems they don't belong to the same session
    # So update doesn't work in tests, we use a workaround
    athlete = Athlete.query.one()
    athlete.update_created_activities_jobs_at.assert_called_once()
    # Should work: assert athlete.created_activities_jobs_at is not None
