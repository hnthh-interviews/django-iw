import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/strategies/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


@pytest.fixture
def strategy(factory, campaign):
    return factory.strategy(campaign=campaign)


def test_response(as_anon, strategy, url):
    response = as_anon.get(url)["results"][0]

    assert response["id"] == strategy.id
    assert response["name"] == strategy.name

    assert set(response) == {
        "campaign",
        "id",
        "name",
    }


def test_campaign_response(as_anon, campaign, strategy, url):
    response = as_anon.get(url)["results"][0]["campaign"]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name

    assert set(response) == {
        "id",
        "name",
    }


@pytest.mark.parametrize("count", [1, 2])
def test_perfomance(as_anon, count, django_assert_num_queries, factory, url):
    factory.cycle(count).strategy()

    with django_assert_num_queries(2):
        as_anon.get(url)


def test_ordering_by_name(as_anon, factory, url):
    factory.cycle(3).strategy(name=(name for name in "bca"))

    response = as_anon.get(url)["results"]

    assert response[0]["name"] == "a"
    assert response[1]["name"] == "b"
    assert response[2]["name"] == "c"
