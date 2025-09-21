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
    result = as_anon.get(url)["results"][0]

    assert result["id"] == strategy.id
    assert result["name"] == strategy.name
    assert set(result) == {
        "campaign",
        "id",
        "name",
    }


@pytest.mark.usefixtures("strategy")
def test_campaign_response(as_anon, campaign, url):
    result = as_anon.get(url)["results"][0]["campaign"]

    assert result["id"] == campaign.id
    assert result["name"] == campaign.name
    assert set(result) == {
        "id",
        "name",
    }


@pytest.mark.parametrize("count", [1, 2])  # noqa: AAA01
def test_perfomance(as_anon, count, django_assert_num_queries, factory, url):
    factory.cycle(count).strategy()

    with django_assert_num_queries(2):
        as_anon.get(url)


def test_ordering_by_name(as_anon, factory, url):
    factory.cycle(3).strategy(name=(name for name in "bca"))

    result = as_anon.get(url)["results"]

    assert result[0]["name"] == "a"
    assert result[1]["name"] == "b"
    assert result[2]["name"] == "c"
