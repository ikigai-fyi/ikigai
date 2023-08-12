from sqlalchemy.orm import scoped_session

from app import db

session_factory: scoped_session = scoped_session(
    session_factory=lambda: db.session, scopefunc=lambda: db.session  # type: ignore
)
