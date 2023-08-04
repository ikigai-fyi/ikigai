import os


class Config(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ENGINE_OPTIONS = {
        # AWS RDS configured with connect_timeout=3600
        "pool_recycle": 3000,
    }

    STRAVA_CLIENT_ID = 106696
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
    STRAVA_WEBHOOK_VALIDATION_TOKEN = os.getenv("STRAVA_WEBHOOK_VALIDATION_TOKEN")
    STRAVA_WEBHOOK_SUBSCRIPTION_ID = (
        int(os.environ["STRAVA_WEBHOOK_SUBSCRIPTION_ID"])
        if os.getenv("STRAVA_WEBHOOK_SUBSCRIPTION_ID")
        else None
    )

    PHONE_NUMBER_PAUL = os.getenv("PHONE_NUMBER_PAUL")
    PHONE_NUMBER_VINCENT = os.getenv("PHONE_NUMBER_VINCENT")
    SENDBLUE_API_KEY = os.getenv("SENDBLUE_API_KEY")
    SENDBLUE_API_SECRET = os.getenv("SENDBLUE_API_SECRET")

    JWT_ACCESS_TOKEN_EXPIRES = False  # FIXME


class ProdConfig(Config):
    APP_ENV = "prod"
    SENTRY_DSN = os.getenv("SENTRY_DSN")


class DevConfig(Config):
    APP_ENV = "dev"
    SENTRY_DSN = os.getenv("SENTRY_DSN")


class LocalConfig(Config):
    APP_ENV = "local"


class TestingConfig(Config):
    APP_ENV = "testing"
    STRAVA_CLIENT_SECRET = "strava_secret"
    STRAVA_WEBHOOK_VALIDATION_TOKEN = "STRAVA_WEBHOOK_VALIDATION_TOKEN"
    STRAVA_WEBHOOK_SUBSCRIPTION_ID = 1
    JWT_SECRET_KEY = "secret"
    SENDBLUE_API_KEY = "key"
    SENDBLUE_API_SECRET = "secret"


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
