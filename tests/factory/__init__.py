from sqlalchemy.orm import scoped_session

from app import db

session_factory = scoped_session(lambda: db.session, scopefunc=lambda: db.session)
