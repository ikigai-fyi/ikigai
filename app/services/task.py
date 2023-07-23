from zappa.asynchronous import task

from app.models.activity import Activity
from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete

from .client import get_strava_client


@task
def fetch_and_store_activities_async(athlete_id: int):
    athlete = Athlete.get_by_id(athlete_id)
    client = get_strava_client(athlete)
    activities_iterator = client.get_activities()

    for activity in activities_iterator:
        is_not_stored = Activity.get_by_strava_id(activity.id) is None
        if is_not_stored and activity.total_photo_count:
            job = ActivityFetchJob(
                athlete_id=athlete.id, activity_strava_id=activity.id
            )
            job.add(commit=True)

    # TODO launch first job
