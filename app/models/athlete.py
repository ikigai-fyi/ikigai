from app import db

from .mixins.base import BaseModelMixin
from .mixins.uuid import UUIDMixin


class Athlete(db.Model, BaseModelMixin, UUIDMixin):  # type: ignore
    __tablename__ = "athlete"
    __uuid_prefix__ = "ath"

    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    picture_url = db.Column(db.String(128))

    strava_id = db.Column(db.BigInteger, nullable=False, index=True, unique=True)
    strava_raw = db.Column(db.JSON(), nullable=False)
    strava_token_id = db.Column(
        db.Integer, db.ForeignKey("strava_token.id"), index=True
    )

    strava_token = db.relationship("StravaToken", backref="athlete")
