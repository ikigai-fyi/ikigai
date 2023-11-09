from flask import current_app
from flask_jwt_extended import create_access_token
from stravalib import Client

from app.models.athlete import Athlete
from app.schemas.inputs.auth import StravaLoginInput
from app.schemas.outputs.auth import StravaLoginOutput
from app.services.activity import get_and_store_random_activity_from_strava
from app.services.task import (
    create_activities_fetch_jobs_async,
    send_welcome_message_async,
)


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

    athlete, created = Athlete.update_or_create(strava_athlete)
    athlete.update_strava_token(
        access_token,
        response["expires_at"],
        response["refresh_token"],
        input.scope,
    )

    if created:
        get_and_store_random_activity_from_strava(athlete)
        create_activities_fetch_jobs_async(athlete.id)
        send_welcome_message_async(athlete.id)

    return StravaLoginOutput(
        athlete=StravaLoginOutput.Athlete.from_orm(athlete),
        jwt=create_access_token(identity=athlete),
    )
