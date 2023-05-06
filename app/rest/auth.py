from flask import Blueprint

from app.extensions import spectree
from app.schemas.inputs.auth import StravaLoginInput
from app.services.auth import login_with_strava

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/login/strava")
@spectree.validate(json=StravaLoginInput)
def ep_strava_login(json: StravaLoginInput):
    return login_with_strava(json).dict()
