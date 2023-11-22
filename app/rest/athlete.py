from flask import Blueprint
from spectree.response import Response

from app.extensions import spectree
from app.models.athlete import Athlete
from app.services.task import create_activities_fetch_jobs_async

athlete = Blueprint("athlete", __name__, url_prefix="/athletes")


@athlete.post("/<string:uuid>/fetch_activities_async")
@spectree.validate(resp=Response("HTTP_200"))
def ep_launch_fetch_activities_async(uuid: str):
    athlete = Athlete.get_by_uuid(uuid)
    create_activities_fetch_jobs_async(athlete.id)
    return "ok"
