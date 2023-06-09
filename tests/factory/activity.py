from datetime import datetime, timedelta

import factory

from app.models.activity import Activity

from . import session_factory
from .athlete import AthleteFactory


class ActivityFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Activity
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"

    name = "Run in the wild"
    sport_type = "Run"
    elapsed_time_in_seconds = factory.Faker("pyint")
    start_datetime = datetime.today() - timedelta(days=10)
    city = factory.Faker("city")

    picture_url = "https://picture.url"
    distance_in_meters = factory.Faker("pyint")
    total_elevation_gain_in_meters = factory.Faker("pyint")
    polyline = factory.Faker("pystr")

    strava_id = factory.Faker("pyint")
    strava_raw: dict = {}

    athlete = factory.SubFactory(AthleteFactory)
