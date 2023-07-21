import random

from geopy.geocoders import Nominatim
from stravalib.model import Activity as StravaActivity

from app.models.activity import Activity
from app.models.athlete import Athlete
from app.schemas.outputs.activity import ActivityOutput
from app.utils.error import NoActivityError

from .auth import current_user, get_logged_strava_client, get_strava_client


def get_random_activity() -> ActivityOutput:
    client = get_logged_strava_client()
    activities: list[StravaActivity] = list(client.get_activities(limit=100))
    if not activities:
        raise NoActivityError

    candidates = [
        activity
        for activity in activities
        if activity.total_photo_count and activity.start_latlng
    ]
    strava_activity = random.choice(candidates)
    activity = fetch_and_store_activity(strava_activity.id, current_user)
    return ActivityOutput.from_orm(activity)


def fetch_and_store_activity(strava_id: int, athlete: Athlete) -> Activity:
    raw_activity = _fetch_raw_activity(strava_id, athlete)
    city = _get_city(raw_activity)
    return Activity.update_or_create_from_strava(raw_activity, city, athlete.id)


def _fetch_raw_activity(strava_id: int, athlete: Athlete) -> dict:
    # When fetching full activities, stravalib might crash when parsing segments
    # The models are generated from Strava OpenAPI specs: https://developers.strava.com/docs/reference/#api-models-SummarySegment
    # It is said than activity_type can be Run or Bike
    # But in practice it happens to also be Hike, Nordic, ...
    # We bypass the response parsing for now
    client = get_strava_client(athlete)
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
    return address.get("city") or address.get("village") or address["town"]
