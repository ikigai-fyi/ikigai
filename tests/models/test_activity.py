import pytest

from tests.factory.activity import ActivityFactory


@pytest.mark.parametrize(("name", "has_custom_name"), [("Test", True)])
def test_has_custom_name(name, has_custom_name):
    assert ActivityFactory(name=name).has_custom_name == has_custom_name
