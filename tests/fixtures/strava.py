import re

import pytest
import responses

from .resources.run import (
    RUN_WITH_PICTURES_DETAIL,
    RUN_WITH_PICTURES_PREVIEW,
    RUN_WITHOUT_PICTURE_PREVIEW,
)
from .resources.bike import BIKE_WITH_PICTURES_DETAIL

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
def get_activities_response_mock_no_activity(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_URL}/athlete/activities",
        json=[],
    )
    yield requests_mock


@pytest.fixture
def get_activities_response_mock_no_picture(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_URL}/athlete/activities",
        json=[RUN_WITHOUT_PICTURE_PREVIEW],
    )
    yield requests_mock


@pytest.fixture
def get_run_activity_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        re.compile(f"{STRAVA_URL}/activities/{RUN_WITH_PICTURES_DETAIL['id']}"),
        json=RUN_WITH_PICTURES_DETAIL,
    )
    yield requests_mock


@pytest.fixture
def get_bike_activity_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        re.compile(f"{STRAVA_URL}/activities/{BIKE_WITH_PICTURES_DETAIL['id']}"),
        json=BIKE_WITH_PICTURES_DETAIL,
    )
    yield requests_mock
