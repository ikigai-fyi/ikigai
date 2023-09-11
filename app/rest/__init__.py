from flask import Blueprint

from .activity import activity
from .auth import auth
from .webhook import webhook

rest = Blueprint("rest", __name__)
rest.register_blueprint(auth)
rest.register_blueprint(activity)
rest.register_blueprint(webhook)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/welcome")
def ep_welcome():
    from app.services.auth import send_welcome_message_async

    # Paul
    send_welcome_message_async(1)
    return {"status": "ok"}
