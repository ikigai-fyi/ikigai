from datetime import datetime, timedelta

import pytest
import responses

from app.services.cron import consume_activities_fetch_queue
from tests.factory.activity_fetch_job import ActivityFetchJob, ActivityFetchJobFactory
from tests.factory.athlete import AthleteFactory
from tests.fixtures.resources.bike import BIKE_WITH_PICTURES_DETAIL
from tests.fixtures.resources.hike import HIKE_WITH_PICTURES_DETAIL
from tests.fixtures.resources.run import RUN_WITH_PICTURES_DETAIL
from tests.fixtures.strava import STRAVA_API_URL


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
    ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=HIKE_WITH_PICTURES_DETAIL["id"],
        do_after=datetime.now() + timedelta(hours=1),
        done_at=None,
    )
    ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=BIKE_WITH_PICTURES_DETAIL["id"],
        canceled_at=datetime.now(),
    )

    consume_activities_fetch_queue()

    assert job_run.done_at is not None
    assert job_run.retry_count == 0

    assert job_bike.done_at is not None
    assert job_bike.retry_count == 0


def test_consume_activities_fetch_queue_retry(requests_mock):
    requests_mock.add(
        responses.GET,
        f"{STRAVA_API_URL}/activities/1234",
        status=400,
        json={},
    )

    athlete = AthleteFactory()
    job = ActivityFetchJobFactory(
        athlete=athlete,
        activity_strava_id=1234,
    )

    consume_activities_fetch_queue()

    # Increase count
    assert job.retry_count == 1
    assert job.canceled_at is None
    assert ActivityFetchJob.query.count() == 1

    consume_activities_fetch_queue()

    # Cancel
    assert job.retry_count == 2  # noqa: PLR2004
    assert job.canceled_at is not None
    assert ActivityFetchJob.query.count() == 1
