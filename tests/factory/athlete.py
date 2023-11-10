from datetime import datetime

import factory

from app.models.athlete import Athlete

from . import session_factory
from .strava_token import StravaTokenFactory


class AthleteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Athlete
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"

    uuid = factory.Faker("pystr")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    picture_url = "https://picture.url"
    updated_from_strava_at = datetime.utcnow()
    last_active_at = datetime.utcnow()

    strava_id = factory.Faker("pyint")
    strava_raw: dict = {}
    strava_token = factory.SubFactory(StravaTokenFactory)
