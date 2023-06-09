from flask import Blueprint, current_app, jsonify

from app.extensions import spectree
from app.schemas.inputs.webhook import StravaWebhookValidationInput
from app.utils.error import UnauthorizedError

webhook = Blueprint("webhook", __name__, url_prefix="/webhooks")


@webhook.get("/strava")
@spectree.validate(query=StravaWebhookValidationInput)
def ep_strava_webhook_validation(query: StravaWebhookValidationInput):
    if query.verify_token != current_app.config["STRAVA_WEBHOOK_VALIDATION_TOKEN"]:
        raise UnauthorizedError

    return jsonify({"hub.challenge": query.challenge})


@webhook.post("/strava")
@spectree.validate()
def ep_strava_webhook():
    1 / 0
    return "ok"
