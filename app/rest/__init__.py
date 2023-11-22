from flask import Blueprint

from .activity import activity
from .athlete import athlete
from .auth import auth
from .webhook import webhook

rest = Blueprint("rest", __name__)
rest.register_blueprint(auth)
rest.register_blueprint(activity)
rest.register_blueprint(webhook)
rest.register_blueprint(athlete)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/popuplate_settings")
def ep_populate_settings():
    from app.models.athlete import Athlete
    from app.models.settings import Settings

    for ath in Athlete.query.all():
        if not ath.settings:
            ath.settings = Settings().add()
            ath.update()

    return {"status": "ok"}
