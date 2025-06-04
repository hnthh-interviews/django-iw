import pytest

from core.testing.api import DRFClient


@pytest.fixture
def as_anon():
    return DRFClient()
