import pytest

from models.models import Strategy


pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/strategies/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


def get_strategy():
    return Strategy.objects.last()


def test_creation(as_anon, campaign, url):
    data = {
        "campaign": campaign.id,
        "name": "new strategy",
    }
    as_anon.post(url, data)

    created = get_strategy()

    assert created.campaign == campaign
    assert created.name == "new strategy"


def test_create_strategy_response(as_anon, campaign, url):
    data = {
        "campaign": campaign.id,
        "name": "one more strategy",
    }
    response = as_anon.post(url, data)

    assert response["name"] == "one more strategy"

    assert set(response) == {
        "campaign",
        "id",
        "name",
    }


def test_create_campaign_response(as_anon, campaign, url):
    data = {
        "campaign": campaign.id,
        "name": "one more strategy",
    }
    response = as_anon.post(url, data)["campaign"]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name

    assert set(response) == {
        "id",
        "name",
    }


def test_create_strategy_without_campaign(as_anon, url):
    data = {
        "name": "bad request strategy",
    }
    response = as_anon.post(url, data)

    assert response.status_code == 400
    assert response["detail"] == "Нельзя создать стратегию без кампании."


def test_create_strategy_without_name(as_anon, campaign, url):
    data = {
        "campaign": campaign.id,
    }
    response = as_anon.post(url, data)

    assert response.status_code == 400
    assert response["detail"] == "Нельзя создать стратегию без имени."


def test_create_strategy_with_nonexistant_campaign(as_anon, url):
    data = {
        "campaign": 999,
        "name": "bad request strategy",
    }
    response = as_anon.post(url, data)

    assert response.status_code == 400
    assert response["detail"] == "Нельзя создать стратегию с несуществующей кампанией."
