import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/campaigns/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


def test_response(as_anon, campaign, url):
    response = as_anon.get(url)["results"][0]  # act

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name
    assert set(response) == {
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

    response = as_anon.get(url)["results"]  # act

    assert response[0]["name"] == "a"
    assert response[1]["name"] == "b"
    assert response[2]["name"] == "c"
