from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from spectree.response import Response

from app.extensions import spectree
from app.services.activity import (
    ActivityOutput,
    get_and_store_random_activity_from_strava,
)

activity = Blueprint("activity", __name__, url_prefix="/activities")


@activity.get("/random")
@spectree.validate(resp=Response(HTTP_200=ActivityOutput))
@jwt_required()
def ep_get_random_activity():
    return jsonify(get_and_store_random_activity_from_strava(current_user))
