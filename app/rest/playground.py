from flask import Blueprint, current_app

from stravalib import Client
from flask_jwt_extended import jwt_required

playground = Blueprint("playground", __name__, url_prefix="/playground")


@playground.get("/paul")
@jwt_required()
def ep_get_paul():
    client = Client()
    response = client.refresh_access_token(
        client_id=current_app.config["STRAVA_CLIENT_ID"],
        client_secret=current_app.config["STRAVA_CLIENT_SECRET"],
        refresh_token=current_app.config["STRAVA_PAUL_REFRESH_TOKEN"],
    )
    client.access_token = response["access_token"]

    athlete = client.get_athlete()
    return athlete.dict()
