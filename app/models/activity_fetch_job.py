from datetime import datetime

from app import db

from .mixins.base import BaseModelMixin


class ActivityFetchJob(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "activity_fetch_job"

    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athlete.id"), index=True, nullable=False
    )
    activity_strava_id = db.Column(db.BigInteger, nullable=False)
    done_at = db.Column(db.DateTime)

    @property
    def is_done(self):
        return self.done_at is not None

    def mark_as_done(self):
        self.done_at = datetime.utcnow()
        self.update()
