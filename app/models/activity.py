from __future__ import annotations

from datetime import datetime

from pydantic.datetime_parse import parse_datetime
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
        db.Integer,
        db.ForeignKey("athlete.id"),
        index=True,
        nullable=False,
    )
    athlete: Mapped[Athlete] = db.relationship(
        "Athlete",
        backref="activities",  # type: ignore
    )

    @classmethod
    def get_by_strava_id(cls, strava_id: int) -> Activity | None:
        return Activity.query.filter_by(strava_id=strava_id).one_or_none()

    @classmethod
    def update_or_create_from_strava(
        cls,
        strava_activity: dict,
        city: str,
        athlete_id: int,
    ) -> Activity:
        activity = cls.get_by_strava_id(strava_activity["id"])
        if not activity:
            activity = Activity()

        picture_url = None
        if primary := strava_activity["photos"]["primary"]:
            picture_url = primary["urls"]["600"]

        activity.name = strava_activity["name"]
        activity.sport_type = strava_activity["sport_type"]
        activity.elapsed_time_in_seconds = strava_activity["moving_time"]
        activity.start_datetime = parse_datetime(strava_activity["start_date"]).replace(
            tzinfo=None,
        )
        activity.city = city
        activity.picture_url = picture_url  # type: ignore
        activity.distance_in_meters = (
            strava_activity["distance"] or None  # type: ignore
        )
        activity.total_elevation_gain_in_meters = (
            strava_activity["total_elevation_gain"] or None  # type: ignore
        )
        activity.polyline = (
            strava_activity["map"]["summary_polyline"] or None  # type: ignore
        )
        activity.strava_id = strava_activity["id"]
        activity.strava_raw = strava_activity
        activity.athlete_id = athlete_id

        activity.add()
        db.session.commit()
        return activity
