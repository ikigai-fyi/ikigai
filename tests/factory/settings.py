import factory

from app.models.settings import Settings

from . import session_factory


class SettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Settings
        sqlalchemy_session = session_factory
        sqlalchemy_session_persistence = "commit"
