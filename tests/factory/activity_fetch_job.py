import factory

from app.models.activity_fetch_job import ActivityFetchJob

from . import session_factory
from .athlete import AthleteFactory


class ActivityFetchJobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ActivityFetchJob
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"

    athlete = factory.SubFactory(AthleteFactory)
    activity_strava_id = 1234
    done_at = None
