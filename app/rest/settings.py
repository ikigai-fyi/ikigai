from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from spectree.response import Response

from app.extensions import spectree
from app.schemas.outputs.settings import SettingsOutput

settings = Blueprint("setting", __name__, url_prefix="/settings")


@settings.get("")
@jwt_required()
@spectree.validate(resp=Response(HTTP_200=SettingsOutput))
def ep_get_settings():
    return SettingsOutput.from_orm(current_user.settings)
