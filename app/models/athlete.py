from app import db

from .mixins.base import BaseModelMixin
from .mixins.uuid import UUIDMixin


class Athlete(db.Model, BaseModelMixin, UUIDMixin):  # type: ignore
    __tablename__ = "athlete"
    __uuid_prefix__ = "ath"
