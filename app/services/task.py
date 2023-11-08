import random
from functools import wraps
from urllib.parse import urljoin

import requests
import sentry_sdk
from flask import current_app
from sendblue import Sendblue
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
def create_activities_fetch_jobs_async(athlete_id: int):
    athlete = Athlete.get_by_id(athlete_id)
    client = get_strava_client(athlete)
    activities_iterator = client.get_activities()

    jobs = [
        ActivityFetchJob(
            athlete_id=athlete.id,
            activity_strava_id=activity.id,
        ).add(commit=True)
        for activity in activities_iterator
        if _should_create_job(activity)
    ]

    # Launch a few random jobs now
    jobs_to_process_now = random.sample(jobs, min(5, len(jobs)))
    for job in jobs_to_process_now:
        process_activity_fetch_job_async(job_id=job.id)

    athlete.update_created_activities_jobs_at()


@task
@with_app_context()
def process_activity_fetch_job_async(job_id: int | None = None):
    job: ActivityFetchJob | None
    if job_id:
        job = ActivityFetchJob.get_by_id(job_id)
    else:
        job = ActivityFetchJob.get_job_to_process()

    if not job:
        return

    athlete = Athlete.get_by_id(job.athlete_id)
    fetch_and_store_activity(job.activity_strava_id, athlete)
    job.mark_as_done()


def _should_create_job(activity) -> bool:
    has_picture = bool(activity.total_photo_count)
    is_not_downloaded = Activity.get_by_strava_id(activity.id) is None
    is_not_pending_download = (
        ActivityFetchJob.get_pending_by_strava_id(activity.id) is None
    )
    return has_picture and is_not_downloaded and is_not_pending_download


@task
@with_app_context()
def send_welcome_message_async(athlete_id: int):
    athlete: Athlete = Athlete.get_by_id(athlete_id)

    try:
        _send_welcome_message_on_telegram(athlete)
    except Exception as e:  # noqa: BLE001
        sentry_sdk.capture_exception(e)

    try:
        _send_welcome_message_on_imessage(athlete)
    except Exception as e:  # noqa: BLE001
        sentry_sdk.capture_exception(e)


def _send_welcome_message_on_telegram(athlete: Athlete):
    url = f"https://api.telegram.org/bot{current_app.config['TELEGRAM_BOT_API_KEY']}/sendPhoto"
    params = {
        "chat_id": -993067240,
        "photo": athlete.picture_url,
        "caption": _format_welcome_message(athlete),
    }

    response = requests.post(url, json=params, timeout=10)
    response.raise_for_status()


def _send_welcome_message_on_imessage(athlete: Athlete):
    args = {
        "numbers": [
            current_app.config["PHONE_NUMBER_VINCENT"],
            current_app.config["PHONE_NUMBER_PAUL"],
        ],
        "content": _format_welcome_message(athlete),
        "media_url": athlete.picture_url,
        "send_style": random.choice(
            [
                "celebration",
                "shooting_star",
                "fireworks",
                "lasers",
                "love",
                "confetti",
                "balloons",
                "spotlight",
                "echo",
                "invisible",
                "gentle",
                "loud",
                "slam",
            ],
        ),
        "status_callback": urljoin(
            current_app.config["SELF_URL"],
            "/rest/webhooks/sendblue/status",
        ),
    }

    Sendblue(
        current_app.config["SENDBLUE_API_KEY"],
        current_app.config["SENDBLUE_API_SECRET"],
    ).send_group_message(args)


def _format_welcome_message(athlete: Athlete) -> str:
    return f"Bienvenue {athlete.first_name} {athlete.last_name}! 🫶 <https://www.strava.com/athletes/{athlete.strava_id}>"
