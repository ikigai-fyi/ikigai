import random

from geopy.geocoders import Nominatim
from pydantic.datetime_parse import parse_datetime
from stravalib.model import Activity as StravaActivity

from app.extensions import db
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

    activity = Activity.get_by_strava_id(strava_id)
    if not activity:
        activity = Activity()

    city = _get_city(raw_activity["start_latlng"][0], raw_activity["start_latlng"][1])

    picture_url = None
    if primary := raw_activity["photos"]["primary"]:
        picture_url = primary["urls"]["600"]

    start_datetime = parse_datetime(raw_activity["start_date"]).replace(tzinfo=None)

    activity.name = raw_activity["name"]
    activity.sport_type = raw_activity["sport_type"]
    activity.elapsed_time_in_seconds = raw_activity["moving_time"]
    activity.start_datetime = start_datetime
    activity.city = city
    activity.picture_url = picture_url
    activity.distance_in_meters = raw_activity["distance"] or None
    activity.total_elevation_gain_in_meters = (
        raw_activity["total_elevation_gain"] or None
    )
    activity.polyline = raw_activity["map"]["summary_polyline"] or None
    activity.strava_id = strava_id
    activity.strava_raw = raw_activity
    activity.athlete_id = current_user.id

    activity.add()
    db.session.commit()

    return activity


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


def _get_city(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="fyi.ikigai")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw["address"]
    return address.get("city") or address["village"]
