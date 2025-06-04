import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/campaigns/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


def test_response(as_anon, campaign, url):
    response = as_anon.get(url)[0]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name

    assert set(response) == {
        "id",
        "name",
    }


@pytest.mark.parametrize("count", [1, 2])
def test_perfomance(as_anon, count, django_assert_num_queries, factory, url):
    factory.cycle(count).campaign()

    with django_assert_num_queries(1):
        as_anon.get(url)
