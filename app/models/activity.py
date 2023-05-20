from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped

from app import db

from .athlete import Athlete
from .mixins.base import BaseModelMixin
from .mixins.uuid import UUIDMixin


class Activity(db.Model, BaseModelMixin, UUIDMixin):  # type: ignore
    __tablename__ = "activity"
    __uuid_prefix__ = "act"

    name: Mapped[str] = db.Column(db.String(128), nullable=False)
    sport_type: Mapped[str] = db.Column(db.String(32), nullable=False)
    elapsed_time_in_seconds: Mapped[int] = db.Column(db.Integer, nullable=False)
    start_datetime: Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    city: Mapped[str] = db.Column(db.String(128), nullable=False)

    picture_url: Mapped[str] = db.Column(db.String(256), index=True)
    distance_in_meters: Mapped[int] = db.Column(db.Integer)
    total_elevation_gain_in_meters: Mapped[int] = db.Column(db.Integer)
    polyline: Mapped[str] = db.Column(db.Text())

    strava_id = db.Column(db.BigInteger, nullable=False, index=True, unique=True)
    strava_raw = db.Column(db.JSON(), nullable=False)

    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athlete.id"), index=True, nullable=False
    )
    athlete: Mapped[Athlete] = db.relationship("Athlete", backref="activities")
