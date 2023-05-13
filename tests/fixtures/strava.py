import pytest
import responses

from .resources.bike import BIKE_WITH_PICTURES_PREVIEW
from .resources.climb import CLIMB_NO_PICTURE_PREVIEW
from .resources.hike import HIKE_WITH_PICTURES_PREVIEW
from .resources.run import RUN_WITH_PICTURES_PREVIEW

STRAVA_URL = "https://www.strava.com/api/v3"


@pytest.fixture
def get_activities_response_mock(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_URL}/athlete/activities",
        json=[
            RUN_WITH_PICTURES_PREVIEW,
            BIKE_WITH_PICTURES_PREVIEW,
            CLIMB_NO_PICTURE_PREVIEW,
            HIKE_WITH_PICTURES_PREVIEW,
        ],
    )
    yield requests_mock
