from datetime import datetime, timedelta

from flask import current_app

from app.models.activity_fetch_job import ActivityFetchJob
from app.models.athlete import Athlete
from app.schemas.inputs.webhook import StravaWebhookInput

# Fetch activity after some delay, to let users time to update pictures
# Since the update webhook is not triggered when adding a picture
FETCH_DELAY_HOURS = 72


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

        # Ignore inactive athlete to preserve Strava API quota
        if not athlete.is_active:
            return

        ActivityFetchJob.delete_scheduled_jobs(athlete.id, input.object_id)
        ActivityFetchJob.create(
            athlete_id=athlete.id,
            activity_strava_id=input.object_id,
            do_after=datetime.utcnow() + timedelta(hours=FETCH_DELAY_HOURS),
        )
