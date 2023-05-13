import pytest
import responses

from .resources.activity import ACTIVITY

STRAVA_URL = "https://www.strava.com/api/v3"


@pytest.fixture
def get_activities_response_mock(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_URL}/athlete/activities",
        json=[ACTIVITY],
    )
    yield requests_mock
