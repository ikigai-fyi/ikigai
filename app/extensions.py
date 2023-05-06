import logging
from http import HTTPStatus
from flask_jwt_extended import JWTManager

import sentry_sdk
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from spectree import SpecTree
from sqlalchemy import MetaData


class _BaseModel(Model):
    def add(self, flush: bool = False, commit: bool = False):
        db.session.add(self)

        if flush:
            db.session.flush()

        if commit:
            db.session.commit()

        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self, commit: bool = False):
        db.session.delete(self)

        if commit:
            db.session.commit()


def register_sentry(app: Flask):
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.WARNING,  # Send warnings & errors as events
    )

    sentry_sdk.init(
        dsn=app.config.get("SENTRY_DSN"),
        integrations=[
            FlaskIntegration(),
            AwsLambdaIntegration(timeout_warning=True),
            sentry_logging,
        ],
        traces_sample_rate=0,
        environment=app.config.get("APP_ENV"),
    )

    sentry_sdk.serializer.MAX_DATABAG_BREADTH = 40


spectree = SpecTree(
    "flask",
    mode="strict",
    path="docs",
    annotations=True,
    validation_error_status=HTTPStatus.BAD_REQUEST,
)


def register_spectree(app: Flask):
    spectree.register(app)


cors = CORS(origins="*", supports_credentials=True)

# CUSTOM - naming convention for keys to avoid upgrade/downgrade issues
# ref : https://github.com/sqlalchemy/alembic/issues/588
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(
    model_class=_BaseModel, metadata=metadata, session_options={"autoflush": False}
)
migrate = Migrate()
jwt = JWTManager()
