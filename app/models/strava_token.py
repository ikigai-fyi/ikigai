from datetime import datetime

from flask import current_app
from stravalib import Client

from app import db

from .mixins.base import BaseModelMixin


class StravaToken(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "strava_token"

    access_token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    scope = db.Column(db.String(128), nullable=False)

    def refresh_if_needed(self):
        if datetime.utcnow() < self.expires_at:
            return

        response = Client().refresh_access_token(
            client_id=current_app.config["STRAVA_CLIENT_ID"],
            client_secret=current_app.config["STRAVA_CLIENT_SECRET"],
            refresh_token=self.refresh_token,
        )

        self.access_token = response["access_token"]
        self.expires_at = datetime.fromtimestamp(response["expires_at"])
        self.refresh_token = response["refresh_token"]
        self.update()
