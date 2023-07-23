from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped
from stravalib.model import Athlete as StravaAthlete

from app import db
from app.extensions import jwt
from app.utils.error import AthleteNotFoundError

from .mixins.base import BaseModelMixin
from .mixins.uuid import UUIDMixin
from .strava_token import StravaToken


class Athlete(db.Model, BaseModelMixin, UUIDMixin):  # type: ignore
    __tablename__ = "athlete"
    __uuid_prefix__ = "ath"

    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    picture_url = db.Column(db.String(256), nullable=False)
    updated_from_strava_at = db.Column(db.DateTime, nullable=False)

    strava_id = db.Column(db.BigInteger, nullable=False, index=True, unique=True)
    strava_raw = db.Column(db.JSON(), nullable=False)
    strava_token_id = db.Column(
        db.Integer, db.ForeignKey("strava_token.id"), index=True
    )

    strava_token: Mapped[StravaToken] = db.relationship(
        "StravaToken", backref="athlete"
    )

    @classmethod
    def get_by_strava_id_or_404(cls, strava_id: int) -> Athlete:
        athlete = Athlete.query.filter_by(strava_id=strava_id).one_or_none()
        if not athlete:
            raise AthleteNotFoundError

        return athlete

    @classmethod
    def update_or_create(cls, strava_athlete: StravaAthlete) -> Athlete:
        athlete = Athlete.query.filter(
            Athlete.strava_id == strava_athlete.id
        ).one_or_none()

        if not athlete:
            athlete = Athlete()

        athlete.first_name = strava_athlete.firstname
        athlete.last_name = strava_athlete.lastname
        athlete.picture_url = strava_athlete.profile
        athlete.updated_from_strava_at = datetime.utcnow()
        athlete.strava_id = strava_athlete.id
        athlete.strava_raw = strava_athlete.json()
        athlete.add()
        db.session.commit()

        return athlete

    def update_strava_token(
        self,
        access_token: str,
        expires_at_timestamp: float,
        refresh_token: str,
        scope: str,
    ) -> StravaToken:
        current_token = self.strava_token
        new_token = StravaToken(
            access_token=access_token,
            expires_at=datetime.fromtimestamp(expires_at_timestamp),
            refresh_token=refresh_token,
            scope=scope,
        ).add()

        self.strava_token = new_token
        self.update()

        if current_token:
            current_token.delete()

        return new_token


@jwt.user_identity_loader
def user_identity_lookup(athlete: Athlete):
    return athlete.uuid


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Athlete.query.filter_by(uuid=identity).one_or_none()
