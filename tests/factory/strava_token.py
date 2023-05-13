from datetime import datetime, timedelta

import factory

from app.models.strava_token import StravaToken

from . import session_factory


class StravaTokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = StravaToken
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"

    access_token = factory.Faker("pystr")
    expires_at = datetime.today() + timedelta(days=1)
    refresh_token = factory.Faker("pystr")
    scope = "profile:read_all,activity:read_all"
