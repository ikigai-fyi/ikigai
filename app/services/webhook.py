from flask import current_app

from app.models.athlete import Athlete
from app.schemas.inputs.webhook import StravaWebhookInput

from .activity import fetch_and_store_activity


def handle_strava_webhook(input: StravaWebhookInput):
    current_app.logger.info(
        "Received Strava webhook",
        extra={
            "object_type": input.object_type.value,
            "aspect_type": input.aspect_type.value,
        },
    )

    if input.is_create_activity or input.is_update_activity:
        athlete = Athlete.get_by_strava_id_or_404(input.owner_id)

        try:
            fetch_and_store_activity(input.object_id, athlete)
        except Exception as e:  # noqa: BLE001
            current_app.logger.warning("Failed to process Strava webhook", exc_info=e)
