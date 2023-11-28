from http import HTTPStatus

from tests.factory.athlete import AthleteFactory


def test_patch_athlete(client):
    athlete = AthleteFactory(email=None)
    response = client.authenticated(athlete).patch(
        "/rest/athletes/self",
        json={"email": "test@test.com"},
    )
    assert response.status_code == HTTPStatus.OK
    assert athlete.email == "test@test.com"


def test_patch_athlete_bad_email(client):
    athlete = AthleteFactory(email=None)
    response = client.authenticated(athlete).patch(
        "/rest/athletes/self",
        json={"email": "test@test"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert athlete.email is None
