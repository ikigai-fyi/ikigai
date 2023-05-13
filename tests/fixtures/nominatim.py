import pytest
import responses


@pytest.fixture
def get_reverse_geocoding_mock(requests_mock):
    requests_mock.add(
        responses.GET,
        "https://nominatim.openstreetmap.org/reverse",
        json={
            "place_id": "100149",
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
            "osm_type": "node",
            "osm_id": "107775",
            "boundingbox": ["51.3473219", "51.6673219", "-0.2876474", "0.0323526"],
            "lat": "51.5073219",
            "lon": "-0.1276474",
            "display_name": "Annecy, France, 74000, France",
            "class": "place",
            "type": "city",
            "importance": 0.9654895765402,
            "icon": "https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png",
            "address": {
                "city": "Annecy",
                "state_district": "Annecy",
                "state": "France",
                "ISO3166-2-lvl4": "GB-ENG",
                "postcode": "74000",
                "country": "France",
                "country_code": "fr",
            },
            "extratags": {
                "capital": "yes",
                "website": "http://www.london.gov.uk",
                "wikidata": "Q84",
                "wikipedia": "en:London",
                "population": "8416535",
            },
        },
    )
    yield requests_mock
