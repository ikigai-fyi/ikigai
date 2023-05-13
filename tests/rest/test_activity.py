from tests.factory.athlete import AthleteFactory


def test_get_random_activity(client):
    athlete = AthleteFactory()
    client.authenticate(athlete)

    response = client.get("/rest/activities/random")
    assert response.status_code == 200
