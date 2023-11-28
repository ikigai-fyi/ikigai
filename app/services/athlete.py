from app.models.athlete import Athlete
from app.schemas.inputs.athlete import PatchAthleteInput


def patch_athlete(athlete: Athlete, input: PatchAthleteInput):
    athlete.email = input.email
    athlete.update()
