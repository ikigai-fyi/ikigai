from http import HTTPStatus

from tests.factory.athlete import AthleteFactory


def test_get_settings(client):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get(
        "/rest/settings",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "refresh_period_in_hours": athlete.settings.refresh_period_in_hours,
    }
