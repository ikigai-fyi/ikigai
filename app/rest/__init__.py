from flask import Blueprint

from app.models.athlete import Athlete

rest = Blueprint("rest", __name__)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/athletes")
def ep_athletes():
    athletes = Athlete.query.all()
    return {"n_athletes": len(athletes)}


@rest.get("/sentry")
def ep_sentry():
    1 / 0
    return {}
