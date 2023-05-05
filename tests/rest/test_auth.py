def test_strava_login(client):
    json = {"code": "", "scope": ""}
    response = client.post("/rest/auth/login/strava", json=json)
    assert response.status_code == 200
    assert response.json == json
