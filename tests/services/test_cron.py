from datetime import datetime

import pytest

from app.services.cron import consume_activities_fetch_queue
from tests.factory.activity_fetch_job import ActivityFetchJobFactory
from tests.factory.athlete import AthleteFactory
from tests.fixtures.resources.bike import BIKE_WITH_PICTURES_DETAIL
from tests.fixtures.resources.hike import HIKE_WITH_PICTURES_DETAIL
from tests.fixtures.resources.run import RUN_WITH_PICTURES_DETAIL


@pytest.mark.usefixtures(
    "get_activity_response_mock_run",
    "get_activity_response_mock_bike",
    "get_reverse_geocoding_mock",
)
def test_consume_activities_fetch_queue():
    athlete = AthleteFactory()
    job_run = ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=RUN_WITH_PICTURES_DETAIL["id"],
    )
    job_bike = ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=BIKE_WITH_PICTURES_DETAIL["id"],
    )

    # Won't be picked up, ensured by no response mock
    ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=HIKE_WITH_PICTURES_DETAIL["id"],
        done_at=datetime.now(),
    )

    consume_activities_fetch_queue()

    assert job_run.done_at is not None
    assert job_bike.done_at is not None
