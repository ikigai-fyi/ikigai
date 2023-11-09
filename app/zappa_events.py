from functools import wraps

from app import create_app
from app.services import cron


def with_app_context():
    def decorator(decorated_function):
        @wraps(decorated_function)
        def wrapper():
            with create_app().app_context():
                return decorated_function()

        return wrapper

    return decorator


@with_app_context()
def consume_activities_fetch_queue():
    cron.consume_activities_fetch_queue()
