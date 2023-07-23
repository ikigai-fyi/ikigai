from flask_jwt_extended import current_user
from stravalib import Client

from app.models.athlete import Athlete
from app.utils.error import MissingStravaAuthenticationError


def get_strava_client(athlete: Athlete) -> Client:
    if not athlete.strava_token:
        raise MissingStravaAuthenticationError

    athlete.strava_token.refresh_if_needed()
    return Client(access_token=athlete.strava_token.access_token)


def get_logged_strava_client() -> Client:
    return get_strava_client(current_user)
