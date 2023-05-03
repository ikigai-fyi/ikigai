def test_ping(client):
    response = client.get("/rest/ping")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_athletes(client):
    response = client.get("/rest/athletes")
    assert response.status_code == 200
    assert response.json == {"n_athletes": 0}
