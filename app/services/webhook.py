from app.schemas.inputs.webhook import StravaWebhookInput
from app.models.athlete import Athlete
from .activity import fetch_and_store_activity


def handle_strava_webhook(input: StravaWebhookInput):
    if input.is_create_activity:
        athlete = Athlete.get_by_strava_id_or_404(input.owner_id)
        fetch_and_store_activity(input.object_id, athlete)
