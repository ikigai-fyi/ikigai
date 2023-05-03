from datetime import datetime

from app.extensions import db


class BaseModelMixin:
    """Database model mixin to add common objects features"""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).one_or_none()
