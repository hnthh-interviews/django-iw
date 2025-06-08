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


def test_response(as_anon, strategy, campaign, url):
    response = as_anon.get(url)["results"][0]

    assert response["id"] == strategy.id
    assert response["name"] == strategy.name
    assert response["campaign"]["id"] == campaign.id
    assert response["campaign"]["name"] == campaign.name

    assert set(response) == {
        "id",
        "campaign",
        "name",
    }
    assert set(response["campaign"]) == {
        "id",
        "name",
    }


@pytest.mark.parametrize("count", [1, 2])
def test_perfomance(as_anon, count, django_assert_num_queries, factory, url):
    factory.cycle(count).strategy()

    with django_assert_num_queries(2):
        as_anon.get(url)


def test_pagination(as_anon, factory, url):
    factory.cycle(101).strategy()

    response = as_anon.get(url)
    response_next_page = as_anon.get(response['next'])

    assert response["count"] == 101
    assert len(response["results"]) == 100
    assert response_next_page["count"] == 101
    assert len(response_next_page["results"]) == 1
