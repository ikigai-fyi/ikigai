from datetime import datetime, timedelta

from pydantic import BaseModel

from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import INACTIVE_DELAY_DAYS, Athlete


class DashboardCard(BaseModel):
    title: str
    content: str


def get_dashboard_cards() -> list[DashboardCard]:
    return [
        _get_active_athletes_count_card(),
        _get_totals_athletes_count_card(),
        _get_queue_size_card(),
        _get_queue_done_card(),
        _get_dead_letter_queue_size_card(),
    ]


def _get_active_athletes_count_card() -> DashboardCard:
    active_count = Athlete.query.filter(
        Athlete.last_active_at.is_not(None),
        Athlete.last_active_at
        > datetime.utcnow() - timedelta(days=INACTIVE_DELAY_DAYS),
    ).count()

    return DashboardCard(
        title=f"🏃‍♂️ Active athletes ({INACTIVE_DELAY_DAYS} days)",
        content=str(active_count),
    )


def _get_totals_athletes_count_card() -> DashboardCard:
    count_athletes = Athlete.query.filter().count()
    return DashboardCard(
        title="👨‍👩‍👧‍👦 Total athletes",
        content=str(count_athletes),
    )


def _get_queue_size_card() -> DashboardCard:
    todo_jobs_count = ActivityFetchJob.query.filter(
        ActivityFetchJob.done_at.is_(None),
        ActivityFetchJob.canceled_at.is_(None),
    ).count()
    return DashboardCard(title="🔄 Jobs to process", content=str(todo_jobs_count))


def _get_queue_done_card() -> DashboardCard:
    done_jobs_count = ActivityFetchJob.query.filter(
        ActivityFetchJob.done_at.is_not(None),
    ).count()
    return DashboardCard(title="✅ Jobs processed", content=str(done_jobs_count))


def _get_dead_letter_queue_size_card() -> DashboardCard:
    canceled_jobs_count = ActivityFetchJob.query.filter(
        ActivityFetchJob.done_at.is_(None),
        ActivityFetchJob.canceled_at.is_not(None),
    ).count()
    return DashboardCard(title="🛑 Jobs canceled", content=str(canceled_jobs_count))
