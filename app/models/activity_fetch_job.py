from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped

from app import db

from .athlete import Athlete
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
    do_after = db.Column(db.DateTime, nullable=False)
    done_at = db.Column(db.DateTime)

    athlete: Mapped[Athlete] = db.relationship(
        "Athlete",
        backref="activity_fetch_jobs",  # type: ignore
    )

    @property
    def is_done(self):
        return self.done_at is not None

    def mark_as_done(self):
        self.done_at = datetime.utcnow()
        self.update()

    @classmethod
    def create(
        cls,
        athlete_id: int,
        activity_strava_id: int,
        do_after: datetime,
    ) -> ActivityFetchJob:
        return ActivityFetchJob(
            athlete_id=athlete_id,
            activity_strava_id=activity_strava_id,
            do_after=do_after,
        ).add(commit=True)

    @classmethod
    def get_jobs_to_process(cls, limit: int) -> list[ActivityFetchJob]:
        return (
            ActivityFetchJob.query.filter(
                ActivityFetchJob.done_at.is_(None),
                ActivityFetchJob.do_after < datetime.utcnow(),
            )
            .limit(limit)
            .all()
        )

    @classmethod
    def get_pending_by_strava_id(
        cls,
        activity_strava_id: int,
    ) -> ActivityFetchJob | None:
        return ActivityFetchJob.query.filter(
            ActivityFetchJob.activity_strava_id == activity_strava_id,
            ActivityFetchJob.done_at.is_(None),
        ).first()
