from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from spectree.response import Response

from app.extensions import spectree
from app.schemas.inputs.settings import SettingsInput
from app.schemas.outputs.settings import SettingsOutput
from app.services.settings import patch_settings

settings = Blueprint("setting", __name__, url_prefix="/settings")


@settings.get("")
@jwt_required()
@spectree.validate(resp=Response(HTTP_200=SettingsOutput))
def ep_get_settings():
    return SettingsOutput.from_orm(current_user.settings)


@settings.patch("")
@jwt_required()
@spectree.validate(json=SettingsOutput, resp=Response(HTTP_200=SettingsOutput))
def ep_patch_settings(json: SettingsInput):
    return patch_settings(current_user, json)
