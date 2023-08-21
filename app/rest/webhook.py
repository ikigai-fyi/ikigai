from flask import Blueprint, current_app, jsonify, request

from app.extensions import spectree
from app.schemas.inputs.webhook import StravaWebhookInput, StravaWebhookValidationInput
from app.services.webhook import handle_strava_webhook
from app.utils.error import UnauthorizedError

webhook = Blueprint("webhook", __name__, url_prefix="/webhooks")


@webhook.get("/strava")
@spectree.validate(query=StravaWebhookValidationInput)
def ep_strava_webhook_validation(query: StravaWebhookValidationInput):
    if query.verify_token != current_app.config["STRAVA_WEBHOOK_VALIDATION_TOKEN"]:
        raise UnauthorizedError

    return jsonify({"hub.challenge": query.challenge})


@webhook.post("/strava")
@spectree.validate(json=StravaWebhookInput)
def ep_strava_webhook(json: StravaWebhookInput):
    # Authenticate webhook using subscription ID
    # It's far from perfect, but Strava does not propose any webhook auth mechanism
    # We assume subscription ID remains a secret
    if json.subscription_id != current_app.config["STRAVA_WEBHOOK_SUBSCRIPTION_ID"]:
        raise UnauthorizedError

    handle_strava_webhook(json)
    return "ok"


@webhook.post("/sendblue/status")
@spectree.validate()
def ep_sendblue_status_webhook():
    current_app.logger.info("Received Sendblue status callback", extra=request.json)
    return "ok"
