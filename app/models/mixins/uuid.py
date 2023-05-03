import shortuuid
from sqlalchemy.ext.declarative import declared_attr

from app.extensions import db

PREFIX_LENGTH = 3
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

shortuuid.set_alphabet(ALPHABET)


class UUIDMixin:
    # Must be overriden by subclasses to be length of 3.
    __uuid_prefix__ = ""
    __uuid_generate__ = True

    @declared_attr
    def uuid(self):
        return db.Column(
            db.String(20),
            nullable=False,
            index=True,
            unique=True,
            default=self.generate_uuid if self.__uuid_generate__ else None,
        )

    @classmethod
    def get_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid).one_or_none()  # type: ignore

    @classmethod
    def generate_uuid(cls) -> str:
        if len(cls.__uuid_prefix__) != PREFIX_LENGTH:
            raise ValueError(f"UUID prefix length must be {PREFIX_LENGTH}")

        uuid = shortuuid.ShortUUID().random(length=16)
        return f"{cls.__uuid_prefix__}_{uuid}"
