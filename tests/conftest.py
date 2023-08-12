from __future__ import annotations

import os

import pytest
import sqlalchemy
from flask import current_app, testing
from flask_jwt_extended import create_access_token
from responses import RequestsMock
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    app_config = os.environ.get("APP_CONFIG")
    if app_config not in {"testing", "sqlite_testing"}:
        # force a valid test config
        os.environ["APP_CONFIG"] = "sqlite_testing"

    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    app.test_client_class = build_test_client_class({})
    with app.test_client() as client:
        yield client


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Add support for ON DELETE CASCADE when testing with sqlite
    # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#foreign-key-support
    if current_app.config["APP_ENV"] == "sqlite_testing":
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@pytest.fixture(scope="session")
def db(app):
    """Session-wide test database."""
    _db.app = app
    if (
        _db.engine.url.host
        and "rds.amazonaws.com" in _db.engine.url.host
        or _db.engine.url.database not in ["TEST_ariane", ":memory:"]
    ):
        raise RuntimeError(
            f"ERROR - your target database {_db.engine.url}"
            "doesn't look like a test DB. "
            "To avoid it to be fully dropped, I'm stopping the test here..",
        )

    try:
        _db.engine.connect()
    except sqlalchemy.exc.OperationalError as e:
        raise RuntimeError(
            f"ERROR - cannot connect to database at {_db.engine.url}. It is running..?",
        ) from e
    _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def db_session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = {"bind": connection, "binds": {}, "autoflush": False}
    session = db._make_scoped_session(options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(autouse=True)
def requests_mock():
    with RequestsMock(assert_all_requests_are_fired=True) as requests_mock_obj:
        yield requests_mock_obj


def build_test_client_class(default_headers: dict):
    class TestClient(testing.FlaskClient):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.default_headers = default_headers

        def open(self, *args, **kwargs):
            headers = kwargs.pop("headers", {}) or {}
            for k, v in self.default_headers.items():
                if k not in headers:
                    headers[k] = v
            kwargs["headers"] = headers
            return super().open(*args, **kwargs)

        def authenticated(self, athlete) -> TestClient:
            jwt = create_access_token(athlete)
            self.default_headers = {**default_headers, "Authorization": f"Bearer {jwt}"}
            return self

    return TestClient


from .pytest.fixtures.nominatim import *  # noqa: E402, F403
from .pytest.fixtures.strava import *  # noqa: E402, F403
