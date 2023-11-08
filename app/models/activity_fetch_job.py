from __future__ import annotations

from datetime import datetime

from app import db

from .mixins.base import BaseModelMixin


class ActivityFetchJob(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "activity_fetch_job"

    athlete_id = db.Column(
        db.Integer,
        db.ForeignKey("athlete.id"),
        index=True,
        nullable=False,
    )
    activity_strava_id = db.Column(db.BigInteger, nullable=False, index=True)
    done_at = db.Column(db.DateTime)

    @property
    def is_done(self):
        return self.done_at is not None

    def mark_as_done(self):
        self.done_at = datetime.utcnow()
        self.update()

    @classmethod
    def get_job_to_process(cls) -> ActivityFetchJob | None:
        return ActivityFetchJob.query.filter(ActivityFetchJob.done_at.is_(None)).first()

    @classmethod
    def get_pending_by_strava_id(
        cls,
        activity_strava_id: int,
    ) -> ActivityFetchJob | None:
        return ActivityFetchJob.query.filter(
            ActivityFetchJob.activity_strava_id == activity_strava_id,
            ActivityFetchJob.done_at.is_(None),
        ).first()

    @classmethod
    def is_queue_empty(cls) -> bool:
        return cls.get_job_to_process() is None
