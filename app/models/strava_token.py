from app import db

from .mixins.base import BaseModelMixin


class StravaToken(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "strava_token"

    access_token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    scope = db.Column(db.String(128), nullable=False)
