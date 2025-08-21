import pytest
from freezegun import freeze_time

pytestmark = pytest.mark.django_db

# Константы для ожидаемого количества компаний
COUNT_ZERO = 0
COUNT_ONE = 1
COUNT_TWO = 2


@pytest.fixture
def url():
    return "/api/v1/agency/campaigns/"


@pytest.fixture
def campaign(factory):
    return factory.campaign()


def test_filter_created_after(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign_1 = factory.campaign(name="beta")
    with freeze_time("2025-08-21T12:00:00"):
        campaign_2 = factory.campaign(name="alpha")

    response = as_anon.get(f"{url}?created_after=2025-08-20")["results"]

    assert len(response) == COUNT_TWO
    assert response[0]["id"] == campaign_2.id
    assert response[1]["id"] == campaign_1.id


def test_filter_created_before(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign_1 = factory.campaign(name="beta")
    with freeze_time("2025-08-21T12:00:00"):
        factory.campaign(name="alpha")

    response = as_anon.get(f"{url}?created_before=2025-08-20T23:59:59")["results"]

    assert len(response) == COUNT_ONE
    assert response[0]["id"] == campaign_1.id


def test_filter_created_after_and_before(as_anon, factory, url):
    # Arrange
    with freeze_time("2025-08-19T12:00:00"):
        factory.campaign(name="delta")
    with freeze_time("2025-08-20T12:00:00"):
        campaign_2 = factory.campaign(name="beta")
    with freeze_time("2025-08-21T12:00:00"):
        campaign_3 = factory.campaign(name="alpha")
    with freeze_time("2025-08-22T12:00:00"):
        factory.campaign(name="gamma")

    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00&created_before=2025-08-21T23:59:59")["results"]

    assert len(response) == COUNT_TWO
    assert response[0]["id"] == campaign_3.id
    assert response[1]["id"] == campaign_2.id


def test_filter_no_results(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-21T00:00:00")["results"]

    assert len(response) == COUNT_ZERO


def test_filter_performance(as_anon, factory, django_assert_num_queries, url):
    with freeze_time("2025-08-20T12:00:00"):
        factory.cycle(3).campaign()

    with django_assert_num_queries(2):
        as_anon.get(f"{url}?created_after=2025-08-19T00:00:00")


def test_filter_invalid_date_format_after(as_anon, url):
    response = as_anon.get(f"{url}?created_after=invalid-date", expected_status_code=400)

    assert "created_after" in response
    assert "Enter a valid date/time." in response["created_after"]


def test_filter_invalid_date_format_before(as_anon, url):
    response = as_anon.get(f"{url}?created_before=invalid-date", expected_status_code=400)

    assert "created_before" in response
    assert "Enter a valid date/time." in response["created_before"]


def test_filter_invalid_date_format_after_and_before(as_anon, url):
    response = as_anon.get(f"{url}?created_after=invalid-date&created_before=invalid-date", expected_status_code=400)

    assert "created_after" in response
    assert "created_before" in response
    assert "Enter a valid date/time." in response["created_after"]
    assert "Enter a valid date/time." in response["created_before"]


def test_filter_no_campaigns(as_anon, url):
    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00")["results"]

    assert len(response) == COUNT_ZERO


def test_filter_ignore_invalid_params_after(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00&invalid_param=123")["results"]

    assert len(response) == COUNT_ONE
    assert response[0]["id"] == campaign.id


def test_filter_ignore_invalid_params_before(as_anon, factory, url):
    with freeze_time("2025-08-21T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_before=2025-08-22T00:00:00&invalid_param=123")["results"]

    assert len(response) == COUNT_ONE
    assert response[0]["id"] == campaign.id


def test_filter_ignore_invalid_params_after_and_before(as_anon, factory, url):
    with freeze_time("2025-08-21T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00&invalid_param=123&created_before=2025-08-22T00:00:00&invalid_param=123")["results"]

    assert len(response) == COUNT_ONE
    assert response[0]["id"] == campaign.id


def test_filter_invalid_date_combination(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-21T00:00:00&created_before=2025-08-20T23:59:59")["results"]

    assert len(response) == COUNT_ZERO


def test_response_fields_after(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00")["results"][0]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name
    assert set(response) == {"id", "name"}


def test_response_fields_before(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_before=2025-08-22T00:00:00")["results"][0]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name
    assert set(response) == {"id", "name"}


def test_response_fields_after_and_before(as_anon, factory, url):
    with freeze_time("2025-08-20T12:00:00"):
        campaign = factory.campaign(name="beta")

    response = as_anon.get(f"{url}?created_after=2025-08-20T00:00:00&created_before=2025-08-22T00:00:00")["results"][0]

    assert response["id"] == campaign.id
    assert response["name"] == campaign.name
    assert set(response) == {"id", "name"}
