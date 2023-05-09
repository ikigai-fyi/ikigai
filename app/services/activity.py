import random

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

    activities = client.get_activities(limit=100)
    activity: model.Activity = random.choice(list(activities))

    return ActivityOutput(
        name=activity.name,
        polyline=activity.map.summary_polyline,
        distance_in_meters=activity.distance,
        elapsed_time_in_seconds=activity.elapsed_time.total_seconds(),
    )
