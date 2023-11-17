from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from spectree.response import Response

from app.extensions import spectree
from app.services.activity import (
    ActivityOutput,
    ActivityPickOutput,
    GetCurrentActivityInput,
    get_current_activity,
    get_random_activity,
    pick_activity,
)

activity = Blueprint("activity", __name__, url_prefix="/activities")


@activity.get("/random")
@spectree.validate(resp=Response(HTTP_200=ActivityOutput))
@jwt_required()
def ep_get_random_activity():
    current_user.update_last_active_at()
    return jsonify(get_random_activity(current_user))


@activity.get("/pick")
@spectree.validate(resp=Response(HTTP_200=ActivityPickOutput))
@jwt_required()
def ep_pick_activity():
    current_user.update_last_active_at()
    return jsonify(pick_activity(current_user))


@activity.get("/current")
@spectree.validate(
    query=GetCurrentActivityInput,
    resp=Response(HTTP_200=ActivityPickOutput),
)
@jwt_required()
def ep_get_current_activity(query: GetCurrentActivityInput):
    current_user.update_last_active_at()
    return jsonify(get_current_activity(current_user, query))
