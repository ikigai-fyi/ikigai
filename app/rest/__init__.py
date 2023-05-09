from flask import Blueprint


from .activity import activity
from .auth import auth

rest = Blueprint("rest", __name__)
rest.register_blueprint(auth)
rest.register_blueprint(activity)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}
