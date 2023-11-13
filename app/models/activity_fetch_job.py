from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped

from app import db

from .athlete import Athlete
from .mixins.base import BaseModelMixin

MAX_RETRY_COUNT = 2


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

    canceled_at = db.Column(db.DateTime)
    retry_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default=0,
    )

    athlete: Mapped[Athlete] = db.relationship(
        "Athlete",
        backref="activity_fetch_jobs",  # type: ignore
    )

    @property
    def is_done(self) -> bool:
        return self.done_at is not None

    @property
    def should_cancel(self) -> bool:
        return self.retry_count >= MAX_RETRY_COUNT

    def mark_as_done(self):
        self.done_at = datetime.utcnow()
        self.update()

    def increase_retry_count(self):
        self.retry_count = self.retry_count + 1
        self.update()

    def cancel(self):
        self.canceled_at = datetime.utcnow()
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
                ActivityFetchJob.canceled_at.is_(None),
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
            ActivityFetchJob.canceled_at.is_(None),
        ).first()

    @classmethod
    def delete_scheduled_jobs(
        cls,
        athlete_id: int,
        activity_strava_id: int,
    ):
        ActivityFetchJob.query.filter(
            ActivityFetchJob.athlete_id == athlete_id,
            ActivityFetchJob.activity_strava_id == activity_strava_id,
            ActivityFetchJob.done_at.is_(None),
            ActivityFetchJob.canceled_at.is_(None),
            ActivityFetchJob.do_after > datetime.utcnow(),
        ).delete()
        db.session.commit()
