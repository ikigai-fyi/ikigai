from flask import Blueprint

from .activity import activity
from .athlete import athlete
from .auth import auth
from .settings import settings
from .webhook import webhook

rest = Blueprint("rest", __name__)
rest.register_blueprint(auth)
rest.register_blueprint(activity)
rest.register_blueprint(webhook)
rest.register_blueprint(athlete)
rest.register_blueprint(settings)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}
