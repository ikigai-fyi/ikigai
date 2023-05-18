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

    activities: list[model.Activity] = list(client.get_activities(limit=50))
    activities_with_picture = [
        activity for activity in activities if activity.total_photo_count
    ]
    activity: model.Activity = random.choice(activities_with_picture)
    picture_urls = _fetch_pictures(client, activity)
    return ActivityOutput(
        name=activity.name,
        city="Annecy",  # FIXME
        sport_type=activity.sport_type,
        picture_urls=picture_urls,
        start_datetime=activity.start_date.replace(tzinfo=None),
        elapsed_time_in_seconds=activity.moving_time.total_seconds(),
        polyline=activity.map.summary_polyline or None,
        distance_in_meters=activity.distance or None,
        total_elevation_gain_in_meters=activity.total_elevation_gain or None,
    )


def _fetch_pictures(client: Client, activity: model.Activity) -> list[str]:
    # When fetching full activities, stravalib might crash when parsing segments
    # The models are generated from Strava OpenAPI specs: https://developers.strava.com/docs/reference/#api-models-SummarySegment
    # It is said than activity_type can be Run or Bike
    # But in practice it happens to also be Hike, Nordic, ...
    # We bypass the response parsing for now
    activity_raw = client.protocol.get(
        "/activities/{id}",
        id=activity.id,
        include_all_efforts=False,
    )
    return [activity_raw["photos"]["primary"]["urls"]["600"]]
