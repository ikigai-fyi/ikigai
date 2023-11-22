from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from spectree.response import Response

from app.extensions import spectree
from app.schemas.inputs.memory import GetCurrentMemoryInput
from app.schemas.outputs.memory import MemoryOutput
from app.services.memory import get_current_memory

memory = Blueprint("memory", __name__, url_prefix="/memories")


@memory.get("/current")
@spectree.validate(
    query=GetCurrentMemoryInput,
    resp=Response(HTTP_200=MemoryOutput),
)
@jwt_required()
def ep_get_current_memory(query: GetCurrentMemoryInput):
    current_user.update_last_active_at()
    return jsonify(get_current_memory(current_user, query))
