from http import HTTPStatus


class BaseError(Exception):
    HTTP_STATUS = HTTPStatus.INTERNAL_SERVER_ERROR
    MESSAGE = {"en": "An error occured", "fr": "Une erreur est survenue"}

    def to_dict(self, lang: str = "en") -> dict:
        return {"type": self.__class__.__name__, "message": self.MESSAGE[lang]}


class MissingStravaAuthenticationError(BaseError):
    HTTP_STATUS = HTTPStatus.BAD_REQUEST
    MESSAGE = {
        "en": "Login with Strava to perform this action",
        "fr": "Connection avec Strava nécessaire pour effectuer cette action",
    }


class UnauthorizedError(BaseError):
    HTTP_STATUS = HTTPStatus.UNAUTHORIZED
    MESSAGE = {
        "en": "Wrong credentials",
        "fr": "Mauvais identifiants",
    }


class AthleteNotFoundError(BaseError):
    HTTP_STATUS = HTTPStatus.NOT_FOUND
    MESSAGE = {
        "en": "Athlete not found",
        "fr": "Athlete inconnu",
    }
