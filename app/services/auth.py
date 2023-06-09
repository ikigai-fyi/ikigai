from flask import current_app
from flask_jwt_extended import create_access_token, current_user
from stravalib import Client

from app.models.athlete import Athlete
from app.schemas.inputs.auth import StravaLoginInput
from app.schemas.outputs.auth import StravaLoginOutput
from app.utils.error import MissingStravaAuthenticationError


def login_with_strava(input: StravaLoginInput) -> StravaLoginOutput:
    client = Client()

    response = client.exchange_code_for_token(
        client_id=current_app.config["STRAVA_CLIENT_ID"],
        client_secret=current_app.config["STRAVA_CLIENT_SECRET"],
        code=input.code,
    )

    access_token = response["access_token"]
    client.access_token = access_token
    strava_athlete = client.get_athlete()

    athlete = Athlete.update_or_create(strava_athlete)
    athlete.update_strava_token(
        access_token, response["expires_at"], response["refresh_token"], input.scope
    )

    return StravaLoginOutput(
        athlete=StravaLoginOutput.Athlete.from_orm(athlete),
        jwt=create_access_token(identity=athlete),
    )


def get_strava_client(athlete: Athlete) -> Client:
    if not athlete.strava_token:
        raise MissingStravaAuthenticationError

    athlete.strava_token.refresh_if_needed()
    return Client(access_token=athlete.strava_token.access_token)


def get_logged_strava_client() -> Client:
    return get_strava_client(current_user)
