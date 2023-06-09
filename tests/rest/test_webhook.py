import faker

fake = faker.Faker()


def test_webhook_validation_unauthorized(client, app):
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={fake.pystr()}&hub.challenge=challenge&hub.mode=subscribe"
    )
    assert response.status_code == 401


def test_webhook_validation(client, app):
    challenge = fake.pystr()
    token = app.config["STRAVA_WEBHOOK_TOKEN"]
    response = client.get(
        f"/rest/webhooks/strava?hub.verify_token={token}&hub.challenge={challenge}&hub.mode=subscribe"
    )

    assert response.status_code == 200
    assert response.json == {"hub.challenge": challenge}
