import re
from datetime import datetime, timedelta

import pytest
import responses

from .resources.bike import BIKE_WITH_PICTURES_DETAIL
from .resources.run import (
    RUN_WITH_PICTURES_DETAIL,
    RUN_WITH_PICTURES_PREVIEW,
    RUN_WITHOUT_PICTURE_PREVIEW,
)

STRAVA_URL = "https://www.strava.com"
STRAVA_API_URL = f"{STRAVA_URL}/api/v3"


@pytest.fixture()
def post_strava_token_response_mock(requests_mock):
    requests_mock.add(
        responses.POST,
        f"{STRAVA_URL}/oauth/token",
        json={
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_at": (datetime.utcnow() + timedelta(days=1)).timestamp(),
        },
    )
    return requests_mock


@pytest.fixture()
def get_strava_athlete_response_mock(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_API_URL}/athlete",
        json={
            "id": 1,
            "firstname": "Firstname",
            "lastname": "Lastname",
            "profile": "picture_url",
        },
    )
    return requests_mock


@pytest.fixture()
def get_activities_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_API_URL}/athlete/activities",
        json=[RUN_WITH_PICTURES_PREVIEW],
    )
    return requests_mock


@pytest.fixture()
def get_activities_response_mock_no_activity(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_API_URL}/athlete/activities",
        json=[],
    )
    return requests_mock


@pytest.fixture()
def get_activities_response_mock_no_picture(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_API_URL}/athlete/activities",
        json=[RUN_WITHOUT_PICTURE_PREVIEW],
    )
    return requests_mock


@pytest.fixture()
def get_run_activity_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        re.compile(f"{STRAVA_API_URL}/activities/{RUN_WITH_PICTURES_DETAIL['id']}"),
        json=RUN_WITH_PICTURES_DETAIL,
    )
    return requests_mock


@pytest.fixture()
def get_bike_activity_response_mock_run(requests_mock):
    requests_mock.add(
        responses.GET,
        re.compile(f"{STRAVA_API_URL}/activities/{BIKE_WITH_PICTURES_DETAIL['id']}"),
        json=BIKE_WITH_PICTURES_DETAIL,
    )
    return requests_mock
