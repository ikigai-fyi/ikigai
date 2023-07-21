from tests.factory.athlete import AthleteFactory
from app.models.activity import Activity
from tests.fixtures.resources.run import RUN_WITH_PICTURES_DETAIL


def test_get_random_activity(
    client,
    get_activities_response_mock_run,
    get_run_activity_response_mock_run,
    get_reverse_geocoding_mock,
):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == 200
    assert response.json == {
        "city": "Annecy",
        "distance_in_meters": 42067,
        "elapsed_time_in_seconds": 13136,
        "name": "Marathon du clair de lune 🌖",
        "picture_url": "https://dgtzuqphqg23d.cloudfront.net/b7G42pDWBelvNgJI1g7GKb1lnKuUB9DEUZ77IZF-qRs-768x576.jpg",
        "polyline": "cskvG}}}d@h@^ShBUv@cCjD}@tD_@|FMhPc@dBUJuE_GqIuNo@}AgBaHoCuEwAiDcC{Q[g@wBiAEm@L]tNoRqATu@mAMAeAlBk@p@iIoEa@o@y@oJQOkDp@}AQ}UkFoLp@{DkCmBSgUrC{Gp@uB|AiBhDoCzCqAXqDF}JqFaIyGaFqBeC^uCSsCXeBlAcDKaH|AcDRsFdBuD[mDfDwB`AwBhBsKQeFtA{Bx@oCfCoArBeC~Ao@?yBcAyC^u@bAgNpYwCvCiErAmMtAkJzC_BrAaArA{BfFaAzAwAn@mEd@}INQa@YGiIAsEj@_FnCwFrE}@jAwBhIy@dAa@tAI~@NpBYnBOIeCiHL{GOYUDsA|BeAhCSBeG}Hg@Qc@Le@h@eIxQ}GbNiC`Du@xAoE|FqDxF_@tAKrDe@bF}FhQy@bBwDvFs@d@aBLsCgB}BpAXvBfApCpCnU|FhQVhBGjAwBf@qIjEwDxDs@bC}@`BaFjBwCgBeDy@yD_@W[Wy@[{E?qMQo@_@FcInNkCvCyA|BiGtGkNxGcGxDoIpD}OjK}Br@yEn@{BxCgBzC[nAq@rAm@n@cIfBmFrBoA?}N~BgC~@kACiFbBkBi@gCp@yEbDwEjG}BjDaCvGyCbCwC~@yA`AoDrEyClCaD`FqNxQ{BvAoIzBuFnCsJrCiD|CYt@UrCeBvDIjDLdEhFdn@|@vAh@xB~@b@lDzDrBv@\\fAa@~@k@h@W|@kAxAmBrAg@bAv@tGQb@}C|@EdBzArGV|C|@zDz@tElAtI~BjKhE|VNrBTn@`@LnBgAj@yANsKIuBJStBpD\\VtA@\\`@~@~Cx@SEmNV_C|@yC|GiIzBdE\\VzAw@rCmDfHiLpHoOjB}F^sGToAfA_CjAq@lEUrCLvDx@xIfD|OxAbGIlCwAdCc@xHDrJ{AdJC|MkCzFVjHbD`Dd@nDa@tGeDxA_@zKG~CNfBb@z@d@jAxAbHxB|@NnAQlAaBnBg@bCqBhEsI`C}BhC{@xGc@pBg@zAcAdMmLl_@_ThByAdCqClCmEnIiV|ByEdEcEbVkNhC}ClBqDxR{h@`@uAZ_EbAg@xAuCpHwRlBuG`OigAnEoT^sDJuDS{F_Gup@zBgPdBiCvB_BrA_@xBSxC\\~BrA|EdFpE|AfAFvCg@nGuBl[kElKsBpKoCr@g@`CWd]}Ir{@mAxEiAhEyB~KgK~AoB~EeEnDoEjCuEpA{C`JwVbEmHtGhCfPj@~DtC~D~A",  # noqa: E501
        "sport_type": "Run",
        "start_datetime": "2023-05-06T18:00:59",
        "total_elevation_gain_in_meters": 242,
        # Deprecated
        "picture_urls": [
            "https://dgtzuqphqg23d.cloudfront.net/b7G42pDWBelvNgJI1g7GKb1lnKuUB9DEUZ77IZF-qRs-768x576.jpg"
        ],
    }

    activity = Activity.query.one()

    assert activity.sport_type == response.json["sport_type"]
    assert activity.elapsed_time_in_seconds == response.json["elapsed_time_in_seconds"]
    assert activity.start_datetime.isoformat() == response.json["start_datetime"]
    assert activity.city == response.json["city"]
    assert activity.picture_url == response.json["picture_url"]
    assert activity.distance_in_meters == response.json["distance_in_meters"]
    assert (
        activity.total_elevation_gain_in_meters
        == response.json["total_elevation_gain_in_meters"]
    )
    assert activity.polyline == response.json["polyline"]

    assert activity.strava_id == RUN_WITH_PICTURES_DETAIL["id"]
    assert activity.strava_raw == RUN_WITH_PICTURES_DETAIL
    assert activity.athlete == athlete


def test_get_random_activity_no_activity(
    client,
    get_activities_response_mock_no_activity,
):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == 400
    assert response.json == {
        "type": "NoActivityError",
        "message": "No activity available on Strava yet",
    }


def test_get_random_activity_no_activity_with_picture(
    client,
    get_activities_response_mock_no_picture,
):
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == 400
    assert response.json == {
        "type": "NoRecentActivityWithPictureError",
        "message": "No recent activity has pictures to be dispayed",
    }
