import random
from datetime import date

from geopy.geocoders import Nominatim
from sqlalchemy import extract
from stravalib.model import Activity as StravaActivity

from app.models.activity import Activity
from app.models.athlete import Athlete
from app.schemas.inputs.activity import GetCurrentActivityInput
from app.schemas.outputs.activity import ActivityOutput
from app.schemas.outputs.pick import ActivityPickOutput, PickType
from app.utils.error import (
    ActivityCityNotFoundError,
    NoActivityError,
    NoRecentActivityWithPictureError,
)

from .client import get_strava_client


def get_current_activity(
    athlete: Athlete,
    input: GetCurrentActivityInput,
) -> ActivityPickOutput:
    refreshed_at = athlete.update_current_activity_refreshed_at(
        force_update=input.refresh,
    )

    # Fix the seed to get deterministic result
    random.seed(refreshed_at.timestamp())

    return pick_activity(athlete)


def pick_activity(athlete: Athlete) -> ActivityPickOutput:
    if activity := get_x_years_ago_activity(athlete):
        return ActivityPickOutput(
            activity=activity,
            pick_type=PickType.X_YEARS_AGO,
        )

    return ActivityPickOutput(
        activity=get_random_activity(athlete),
        pick_type=PickType.RANDOM,
    )


def get_x_years_ago_activity(athlete: Athlete) -> ActivityOutput | None:
    candidates = Activity.query.filter(
        Activity.athlete_id == athlete.id,
        Activity.picture_url.is_not(None),
        extract("day", Activity.start_datetime) == date.today().day,
        extract("month", Activity.start_datetime) == date.today().month,
        extract("year", Activity.start_datetime) < date.today().year,
    ).all()
    if not candidates:
        return None

    activity = random.choice(candidates)
    return ActivityOutput.from_orm(activity)


def get_random_activity(athlete: Athlete) -> ActivityOutput:
    candidates: list[Activity] = Activity.query.filter(
        Activity.athlete_id == athlete.id,
        Activity.picture_url.is_not(None),
    ).all()
    if not candidates:
        raise NoRecentActivityWithPictureError

    activity = random.choice(candidates)
    return ActivityOutput.from_orm(activity)


def get_and_store_random_activity_from_strava(athlete: Athlete) -> ActivityOutput:
    strava_activity = get_random_activity_from_strava(athlete)
    activity = fetch_and_store_activity(strava_activity.id, athlete)
    return ActivityOutput.from_orm(activity)


def get_random_activity_from_strava(athlete: Athlete) -> StravaActivity:
    client = get_strava_client(athlete)

    activities: list[StravaActivity] = list(client.get_activities(limit=100))
    if not activities:
        raise NoActivityError

    activities_with_picture = [
        activity for activity in activities if activity.total_photo_count
    ]
    if not activities_with_picture:
        raise NoRecentActivityWithPictureError

    return random.choice(activities_with_picture)


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
    # Retro-compat until we handle NULL cities in app
    if not strava_activity["start_latlng"]:
        return ""

    lat, lon = strava_activity["start_latlng"][0], strava_activity["start_latlng"][1]
    geolocator = Nominatim(user_agent="fyi.ikigai")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw["address"]

    fields_lookup_by_priority = ["city", "village", "town", "hamlet", "suburb", "state"]
    for field in fields_lookup_by_priority:
        if field in address:
            return address[field]

    raise ActivityCityNotFoundError
