import random

import sentry_sdk
from flask_jwt_extended import current_user
from stravalib import Client, model

from app.models.athlete import Athlete
from app.schemas.outputs.activity import ActivityOutput
from app.utils.error import MissingStravaAuthenticationError


def get_random_activity() -> ActivityOutput:
    athlete: Athlete = current_user
    if not athlete.strava_token:
        raise MissingStravaAuthenticationError

    athlete.strava_token.refresh_if_needed()
    client = Client(access_token=athlete.strava_token.access_token)

    activities: list[model.Activity] = list(client.get_activities(limit=30))
    activities_with_picture = [
        activity for activity in activities if activity.total_photo_count
    ]
    activity: model.Activity = random.choice(activities_with_picture)

    try:
        activity = client.get_activity(activity.id)
        picture_urls = [activity.photos.primary.urls["600"]]
    except Exception as e:
        # There is an issue with stravalib and Hike activities
        # When fetching full, parsing is failing
        sentry_sdk.capture_exception(e)
        picture_urls = ["https://picsum.photos/200"]

    return ActivityOutput(
        name=activity.name,
        city="Annecy",  # FIXME
        sport_type=activity.sport_type,
        picture_urls=picture_urls,
        start_datetime=activity.start_date.replace(tzinfo=None),
        elapsed_time_in_seconds=activity.elapsed_time.total_seconds(),
        polyline=activity.map.summary_polyline or None,
        distance_in_meters=activity.distance or None,
        total_elevation_gain_in_meters=activity.total_elevation_gain or None,
    )
