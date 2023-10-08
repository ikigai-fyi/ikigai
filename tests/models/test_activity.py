import pytest

from tests.factory.activity import ActivityFactory


@pytest.mark.parametrize(
    "name",
    [
        "Oppvarming + drills + 3 SL",
        "Warm up",
    ],
)
def test_has_custom_name(name):
    assert ActivityFactory(name=name).has_custom_name


@pytest.mark.parametrize(
    "name",
    [
        "Morning Run",
        "Morning Ride",
        "Morning Walk",
        "Morning Workout",
        "Morning Trail Run",
        "Morning Weight Training",
        "Morning Yoga",
        "Morning Swim",
        "Course à pied le matin",
        "Sortie vélo le matin",
        "Lunch Run",
        "Lunch Ride",
        "Lunch Walk",
        "Lunch Workout",
        "Lunch Trail Run",
        "Lunch Hike",
        "Course à pied le midi",
        "Afternoon Run",
        "Afternoon Ride",
        "Afternoon Walk",
        "Afternoon Workout",
        "Afternoon Trail Run",
        "Afternoon Yoga",
        "Afternoon Hike",
        "Afternoon Swim",
        "Sortie vélo dans l'après-midi",
        "Course à pied dans l'après-midi",
        "Natation dans l'après-midi",
        "Evening Run",
        "Evening Ride",
        "Evening Walk",
        "Evening Workout",
        "Evening Trail Run",
        "Evening Weight Training",
        "Evening Swim",
        "Course à pied en soirée",
        "Natation en soirée",
        "Night Run",
        "Night Walk",
    ],
)
def test_has_not_custom_name(name):
    assert not ActivityFactory(name=name).has_custom_name
