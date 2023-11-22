from http import HTTPStatus

from tests.factory.athlete import AthleteFactory
from tests.factory.settings import SettingsFactory


def test_get_settings(client):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get(
        "/rest/settings",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "refresh_period_in_hours": athlete.settings.refresh_period_in_hours,
    }


def test_patch_settings(client):
    settings_1 = SettingsFactory()
    athlete = AthleteFactory(settings=settings_1)

    settings_2 = SettingsFactory(
        refresh_period_in_hours=settings_1.refresh_period_in_hours + 1,
    )
    response = client.authenticated(athlete).patch(
        "/rest/settings",
        json={
            "refresh_period_in_hours": settings_2.refresh_period_in_hours,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "refresh_period_in_hours": settings_2.refresh_period_in_hours,
    }
    assert (
        athlete.settings.refresh_period_in_hours == settings_2.refresh_period_in_hours
    )
