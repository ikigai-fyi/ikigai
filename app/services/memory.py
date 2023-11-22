import random

from app.models.athlete import Athlete
from app.schemas.inputs.memory import GetCurrentMemoryInput
from app.schemas.outputs.memory import MemoryOutput

from .activity import pick_activity


def get_current_memory(
    athlete: Athlete,
    input: GetCurrentMemoryInput,
) -> MemoryOutput:
    athlete.refresh_memory_if_needed(
        force_update=input.refresh,
    )

    # Fix the seed to get deterministic result
    random.seed(athlete.memory_refreshed_at.timestamp())

    return pick_activity(athlete)
