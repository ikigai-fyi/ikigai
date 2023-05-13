import random

from tests.factory.athlete import AthleteFactory


def test_get_random_activity(
    client, get_activities_response_mock, get_activity_response_mock
):
    random.seed(42)
    athlete = AthleteFactory()
    response = client.authenticated(athlete).get("/rest/activities/random")

    assert response.status_code == 200
    assert response.json == {
        "city": "Annecy",
        "distance_in_meters": 11361,
        "elapsed_time_in_seconds": 14175,
        "name": "Randonnée le matin",
        "picture_urls": [
            "https://dgtzuqphqg23d.cloudfront.net/b7G42pDWBelvNgJI1g7GKb1lnKuUB9DEUZ77IZF-qRs-768x576.jpg"
        ],
        "polyline": "onkvGikpd@?Yf@I`As@Jb@Af@HRbBbA|Dp@rAb@n@`@v@JfBQlA}At@WtCIdCJ\\OjAEdAFLROrAPz@Ul@C~AJHPlA~@~A`@\\n@EzA]t@b@vAX|@YlDI~@g@\\e@l@a@f@}APkBEaAHsAI_@N[XQt@Hp@SN{@@iAVkBGA@OLc@HiDH_BZEFcALMFUDc@PUG@BQa@yA\\e@Vo@x@F|BGP[b@EJQn@a@b@KzAV`@XlBGz@S^[b@Bc@@KNm@e@ALSEs@u@g@KK[CJFKLFLKn@N`@GKDQYYKE[a@E{@uAMo@f@Cf@V^@GEZE|@h@O_A\\OFWTMTDl@a@tEqAVMHw@LOp@Gr@i@XB`@WnAZdBn@bBF~@nBTTv@Pn@?lBg@d@]tBm@rAcAlAA@q@SWPFTSL_@?e@_@Ya@u@kBa@iAi@a@u@E_@A}@f@Kp@sAXMDUZYwAYkBuA{@}@RWT?^k@f@Ut@m@gBgAEKWGGYWMh@e@o@s@LDGMk@]FSf@YA]UCGa@q@KAi@USXUMI@QF?@POXLTEHZH@XTHh@h@E\\_@p@p@p@Zb@e@^Xf@~BzAeBbBeA^rBjBvAt@z@P}@`Bc@h@{@h@AFNHAb@b@t@L?d@j@rB\\vA~AIn@U^Ax@KZeABaBhAiANaAl@mBh@mA?q@Ya@c@Ou@U[oDi@uAk@q@DgB`Am@pAoBn@iCb@i@RYb@i@DPbAk@@_Ci@SH`@bA|BfBGGg@Vu@ASKVZx@j@r@VdA@RGNJGNs@Je@\\s@JYGSR[@m@_@UFu@g@YCgAv@KReB^g@?g@O]H[Y]uAAaAK[Dm@EeAFGGk@oBMGQg@EGSE@CSe@OOSi@BoAz@CLGEy@f@u@BcA~@y@R[c@WKkAIw@Ae@Ma@_@i@SUa@a@?i@`@{AjCQh@s@Ni@\\QTuGr@kC]wBZaB[sD{Bu@oAYO{Df@{AYWFw@a@k@DkBW_A^_A~@{@NmAOGHFLrAb@rBrAE^YXeAXcDdBeC`@hCi@tAaAjA]PQp@GPl@u@zC?`@JLEz@Pt@ITl@hCDxAPnAZzFAv@RDCFLMb@C|AX@ZWL?Pe@?i@I",  # noqa: E501
        "sport_type": "Hike",
        "start_datetime": "2023-05-02T08:12:00",
        "total_elevation_gain_in_meters": 856,
    }
