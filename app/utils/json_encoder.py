from datetime import date, datetime, time
from decimal import Decimal

from flask.json.provider import DefaultJSONProvider
from flask.json.provider import _default as flask_default
from pydantic import BaseModel


def _default(obj):
    # Serialize date and datetime objects to ISO 8601
    if isinstance(obj, date | datetime | time):
        return obj.isoformat()

    # Serialize Decimal objects to floats
    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, BaseModel):
        return obj.dict()

    return flask_default(obj)


class JSONEncoder(DefaultJSONProvider):
    default = staticmethod(_default)  # type: ignore[assignment]
