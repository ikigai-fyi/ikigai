import random

from geopy.geocoders import Nominatim
from stravalib.model import Activity as StravaActivity

from app.models.activity import Activity
from app.schemas.outputs.activity import ActivityOutput

from .auth import current_user, get_logged_strava_client


def get_random_activity() -> ActivityOutput:
    client = get_logged_strava_client()
    activities: list[StravaActivity] = list(client.get_activities(limit=100))
    activities_with_picture = [
        activity for activity in activities if activity.total_photo_count
    ]
    strava_activity = random.choice(activities_with_picture)
    activity = _fetch_and_store_activity(strava_activity.id)
    return ActivityOutput.from_orm(activity)


def _fetch_and_store_activity(strava_id: int) -> Activity:
    raw_activity = _fetch_raw_activity(strava_id)
    city = _get_city(raw_activity)
    return Activity.update_or_create_from_strava(raw_activity, city, current_user)


def _fetch_raw_activity(strava_id: int) -> dict:
    # When fetching full activities, stravalib might crash when parsing segments
    # The models are generated from Strava OpenAPI specs: https://developers.strava.com/docs/reference/#api-models-SummarySegment
    # It is said than activity_type can be Run or Bike
    # But in practice it happens to also be Hike, Nordic, ...
    # We bypass the response parsing for now
    client = get_logged_strava_client()
    return client.protocol.get(
        "/activities/{id}",
        id=strava_id,
        include_all_efforts=False,
    )


def _get_city(strava_activity: dict) -> str:
    lat, lon = strava_activity["start_latlng"][0], strava_activity["start_latlng"][1]
    geolocator = Nominatim(user_agent="fyi.ikigai")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw["address"]
    return address.get("city") or address["village"]
