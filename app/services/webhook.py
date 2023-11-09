from flask import current_app

from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete
from app.schemas.inputs.webhook import StravaWebhookInput


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
        ActivityFetchJob.create(
            athlete_id=athlete.id,
            activity_strava_id=input.object_id,
        )
