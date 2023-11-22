from app import db

from .mixins.base import BaseModelMixin


class Settings(db.Model, BaseModelMixin):  # type: ignore
    __tablename__ = "settings"

    refresh_period_in_hours = db.Column(db.Integer, nullable=False, default=24)
