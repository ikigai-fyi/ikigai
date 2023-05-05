from flask import Blueprint

from app.models.athlete import Athlete

from .playground import playground

rest = Blueprint("rest", __name__)
rest.register_blueprint(playground)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/athletes")
def ep_athletes():
    athletes = Athlete.query.all()
    return {"n_athletes": len(athletes)}
