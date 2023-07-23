from app import db

from .mixins.base import BaseModelMixin


class ActivityFetchJob(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "activity_fetch_job"

    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athlete.id"), index=True, nullable=False
    )
    activity_strava_id = db.Column(db.BigInteger, nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)

    def mark_as_done(self):
        self.done = True
        self.update()
