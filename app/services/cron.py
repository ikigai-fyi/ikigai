from app.models.activity_fetch_job import ActivityFetchJob

from .task import process_activity_fetch_job_async

CONSUMPTION_BURST = 5


def consume_activities_fetch_queue():
    """We assume this is only called sequentially
    so that the same job cannot be consumed twice in parallel.
    """
    jobs = ActivityFetchJob.get_jobs_to_process(CONSUMPTION_BURST)
    for job in jobs:
        process_activity_fetch_job_async(job.id)
