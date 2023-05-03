import logging
import os

from flask import Flask

from app.config import CONFIGURATIONS
from app.extensions import cors, db, migrate


def register_extensions(app: Flask):
    """Init all extensions."""
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask):
    """Register blueprints."""
    from app.rest import rest as rest_blueprint

    app.register_blueprint(rest_blueprint, url_prefix="/rest")


def create_app() -> Flask:
    """Application factory that create a flask app."""
    app = Flask(__name__)

    # Keep root logging level to ERROR only
    # We don't want to display libraries logs by default
    logging.getLogger().setLevel(logging.ERROR)
    log_level = logging.getLevelName(os.getenv("LOG_LEVEL") or "INFO")
    app.logger.level = log_level

    with app.app_context():
        config_name = os.getenv("APP_CONFIG")
        if config_name is None:
            raise Exception("Missing APP_CONFIG environment")

        app.config.from_object(CONFIGURATIONS[config_name])

        register_extensions(app)
        register_blueprints(app)

        return app
