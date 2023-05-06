from app.schemas.inputs.auth import StravaLoginInput
from app.schemas.outputs.auth import StravaLoginOutput
from stravalib import Client
from flask import current_app

from app.models.athlete import Athlete


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

    return StravaLoginOutput(athlete=StravaLoginOutput.Athlete.from_orm(athlete))
