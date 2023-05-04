import os


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ENGINE_OPTIONS = {
        # AWS RDS configured with connect_timeout=3600
        "pool_recycle": 3000,
    }


class ProdConfig(Config):
    APP_ENV = "prod"


class DevConfig(Config):
    APP_ENV = "dev"


class LocalConfig(Config):
    APP_ENV = "local"


class TestingConfig(Config):
    APP_ENV = "testing"


class SQLiteTestingConfig(TestingConfig):
    APP_ENV = "sqlite_testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI_PRICING_ANALYSIS = "sqlite:///:memory:"


CONFIGURATIONS = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "local": LocalConfig,
    "testing": TestingConfig,
    "sqlite_testing": SQLiteTestingConfig,
    "default": LocalConfig,
}
