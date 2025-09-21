import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/campaigns/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


def test_response(as_anon, campaign, url):
    result = as_anon.get(url)["results"][0]

    assert result["id"] == campaign.id
    assert result["name"] == campaign.name
    assert set(result) == {
        "id",
        "name",
    }


@pytest.mark.parametrize("count", [1, 2])  # noqa: AAA01
def test_perfomance(as_anon, count, django_assert_num_queries, factory, url):
    factory.cycle(count).campaign()

    with django_assert_num_queries(2):
        as_anon.get(url)


def test_ordering_by_name(as_anon, factory, url):
    factory.cycle(3).campaign(name=(name for name in "bca"))

    result = as_anon.get(url)["results"]

    assert result[0]["name"] == "a"
    assert result[1]["name"] == "b"
    assert result[2]["name"] == "c"
