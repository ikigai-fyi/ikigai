from flask import Blueprint


from .activity import activity
from .auth import auth

rest = Blueprint("rest", __name__)
rest.register_blueprint(auth)
rest.register_blueprint(activity)


@rest.get("/ping")
def ep_ping():
    return {"status": "ok"}


@rest.get("/test/<usecase>")
def ep_test(usecase):
    from app.utils.error import BaseError
    from http import HTTPStatus

    class MyBadRequest(BaseError):
        HTTP_STATUS = HTTPStatus.BAD_REQUEST
        MESSAGE = {"en": "Oups"}

    class MyCustomThingy(Exception):
        pass

    if usecase == "bad":
        raise MyBadRequest
    else:
        raise MyCustomThingy

    return {"status": "ok"}
