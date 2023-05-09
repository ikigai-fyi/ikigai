from http import HTTPStatus


class BaseError:
    HTTP_STATUS = HTTPStatus.INTERNAL_SERVER_ERROR
    MESSAGE = {"en": "An error occured", "fr": "Une erreur est survenue"}

    def to_dict(self, lang: str = "en") -> dict:
        return {"type": self.__class__.__name__, "message": self.MESSAGE[lang]}
