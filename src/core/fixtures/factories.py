import pytest

from core.testing.factories import FixtureFactory


@pytest.fixture
def factory():
    return FixtureFactory()
