import re

import pytest
import responses

from .resources.run import RUN_WITH_PICTURES_DETAIL, RUN_WITH_PICTURES_PREVIEW

STRAVA_URL = "https://www.strava.com/api/v3"


@pytest.fixture
def get_activities_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_URL}/athlete/activities",
        json=[RUN_WITH_PICTURES_PREVIEW],
    )
    yield requests_mock


@pytest.fixture
def get_activity_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        re.compile(f"{STRAVA_URL}/activities/{RUN_WITH_PICTURES_DETAIL['id']}"),
        json=RUN_WITH_PICTURES_DETAIL,
    )
    yield requests_mock
