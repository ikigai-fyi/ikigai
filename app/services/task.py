from functools import wraps
from typing import Optional

from zappa.asynchronous import task

from app import create_app
from app.models.activity import Activity
from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete

from .activity import fetch_and_store_activity
from .client import get_strava_client


def with_app_context():
    def decorator(decorated_function):
        @wraps(decorated_function)
        def wrapper(*args, **kwargs):
            with create_app().app_context():
                return decorated_function(*args, **kwargs)

        return wrapper

    return decorator


@task
@with_app_context()
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

    # Launch the first job
    job_id = job.id if job else None
    process_activity_fetch_job_async(job_id)


@task
@with_app_context()
def process_activity_fetch_job_async(job_id: Optional[int] = None):
    job: Optional[ActivityFetchJob]
    if job_id:
        job = ActivityFetchJob.get_by_id(job_id)
    else:
        job = ActivityFetchJob.get_job_to_process()

    if (not job) or (job and job.is_done):
        # What's next?
        if not ActivityFetchJob.is_queue_empty():
            process_activity_fetch_job_async()

        return

    athlete = Athlete.get_by_id(job.athlete_id)
    fetch_and_store_activity(job.activity_strava_id, athlete)
    job.mark_as_done()

    # What's next?
    process_activity_fetch_job_async()
