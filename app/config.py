import os


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")


class ProductionConfig(Config):
    APP_ENV = "production"


class DevelopmentConfig(Config):
    APP_ENV = "development"


class LocalConfig(Config):
    APP_ENV = "local"


class TestingConfig(Config):
    APP_ENV = "testing"


class SQLiteTestingConfig(TestingConfig):
    APP_ENV = "sqlite_testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI_PRICING_ANALYSIS = "sqlite:///:memory:"


CONFIGURATIONS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "local": LocalConfig,
    "testing": TestingConfig,
    "sqlite_testing": SQLiteTestingConfig,
    "default": LocalConfig,
}
