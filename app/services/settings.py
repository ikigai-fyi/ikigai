from app.models.athlete import Athlete
from app.schemas.inputs.settings import SettingsInput
from app.schemas.outputs.settings import SettingsOutput


def patch_settings(athlete: Athlete, input: SettingsInput) -> SettingsOutput:
    # FIXME do something more elegant to enable:
    # 1. Partial data patching
    # 2. Handle new fields without changing the code
    athlete.settings.refresh_period_in_hours = input.refresh_period_in_hours
    athlete.settings.update()
    return SettingsOutput.from_orm(athlete.settings)
