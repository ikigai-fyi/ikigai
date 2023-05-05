from app.schemas.inputs.auth import StravaLoginInput
from stravalib import Client
from flask import current_app
from app.models.athlete import Athlete
from datetime import datetime


def login_with_strava(input: StravaLoginInput):
    client = Client()

    response = client.exchange_code_for_token(
        client_id=current_app.config["STRAVA_CLIENT_ID"],
        client_secret=current_app.config["STRAVA_CLIENT_SECRET"],
        code=input.code,
    )

    access_token = response["access_token"]
    client.access_token = access_token
    strava_athlete = client.get_athlete()

    athlete = Athlete.query.filter(Athlete.strava_id == strava_athlete.id).one_or_none()
    if not athlete:
        athlete = Athlete()

    athlete.first_name = strava_athlete.firstname
    athlete.last_name = strava_athlete.lastname
    athlete.picture_url = strava_athlete.profile
    athlete.strava_id = strava_athlete.id
    athlete.strava_access_token = access_token
    athlete.strava_access_token_expires_at = datetime.fromtimestamp(
        response["expires_at"]
    )
    athlete.strava_refresh_token = response["refresh_token"]
    athlete.strava_scope = input.scope
    athlete.strava_raw = strava_athlete.json()
    athlete.add()
    athlete.update()

    return {
        "uuid": athlete.uuid,
        "first_name": athlete.first_name,
        "last_name": athlete.last_name,
        "picture_url": athlete.picture_url,
    }
