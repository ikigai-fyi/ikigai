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
        city="Annecy",  # FIXME
        sport_type=activity.sport_type,
        picture_urls=["https://picsum.photos/200"],
        elapsed_time_in_seconds=activity.elapsed_time.total_seconds(),
        polyline=activity.map.summary_polyline or None,
        distance_in_meters=activity.distance or None,
        total_elevation_gain_in_meters=activity.total_elevation_gain or None,
    )
