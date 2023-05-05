from flask import Blueprint

from app.extensions import spectree
from app.schemas.inputs.auth import StravaLoginInput

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/login/strava")
@spectree.validate(json=StravaLoginInput)
def ep_strava_login(json: StravaLoginInput):
    return json.dict()
