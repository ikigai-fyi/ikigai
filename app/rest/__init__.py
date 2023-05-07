from flask import Blueprint

from app.models.athlete import Athlete

from .activity import activity
from .auth import auth
from .playground import playground

rest = Blueprint("rest", __name__)
rest.register_blueprint(playground)
rest.register_blueprint(auth)
rest.register_blueprint(activity)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/athletes")
def ep_athletes():
    athletes = Athlete.query.all()
    return {"n_athletes": len(athletes)}
