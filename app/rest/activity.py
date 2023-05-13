from flask import Blueprint
from spectree.response import Response

from app.extensions import spectree
from flask_jwt_extended import jwt_required
from app.services.activity import ActivityOutput, get_random_activity

activity = Blueprint("activity", __name__, url_prefix="/activities")


@activity.get("/random")
@spectree.validate(resp=Response(HTTP_200=ActivityOutput))
@jwt_required()
def ep_get_random_activity():
    return get_random_activity()
