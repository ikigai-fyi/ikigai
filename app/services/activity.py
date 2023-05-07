import random

from flask import abort
from flask_jwt_extended import current_user
from stravalib import Client, model

from app.models.athlete import Athlete
from app.schemas.outputs.activity import ActivityOutput


def get_random_activity() -> ActivityOutput:
    athlete: Athlete = current_user

    # FIXME: handle in case user revoked Strava auth
    if not athlete.strava_token:
        abort(400)

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
