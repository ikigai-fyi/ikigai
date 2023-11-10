from datetime import datetime

import factory

from app.models.activity_fetch_job import ActivityFetchJob

from . import session_factory


class ActivityFetchJobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ActivityFetchJob
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"

    activity_strava_id = 1234
    do_after = datetime.utcnow()
    done_at = None
