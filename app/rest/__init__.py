from flask import Blueprint

rest = Blueprint("rest", __name__)


@rest.get("/ping")
def ep_ping():
    return "pong"
