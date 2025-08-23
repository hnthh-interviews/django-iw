from datetime import timedelta as td
from http import HTTPStatus

import pytest
from django.utils import timezone
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


@pytest.fixture
def url():
    return "/api/v1/agency/campaigns/"


@pytest.fixture(autouse=True)
def create_campaigns_with_different_dates(factory):
    test_date = timezone.datetime(2025, 8, 20, tzinfo=timezone.get_current_timezone())
    dates = (test_date - td(days=1), test_date, test_date + td(days=1))
    campaigns = []
    for i, date in enumerate(dates, start=1):
        with freeze_time(date):
            campaigns.append(factory.campaign(name=f"campaign{i}"))
    return campaigns


@pytest.mark.parametrize(
    ("filter_option", "expected_campaign_name"),
    [
        ({"created_at_after": "2025-08-20"}, ["campaign2", "campaign3"]),
        ({"created_at_before": "2025-08-20"}, ["campaign1", "campaign2"]),
        ({"created_at_before": "2025-08-18", "created_at_after": "2025-08-22"}, []),
    ],
)
def test_filter_by_date(as_anon, url, filter_option, expected_campaign_name):
    response = as_anon.get(url, filter_option)
    results = [x["name"] for x in response["results"]]

    assert results == expected_campaign_name


@pytest.mark.parametrize(
    "filter_option",
    [
        {"created_at_after": "2025-13-32"},
        {"created_at_before": "2025-13-32"},
    ],
)
def test_filter_with_invalid_params(as_anon, url, filter_option):
    response = as_anon.get(url, filter_option, expected_status_code=HTTPStatus.BAD_REQUEST)

    assert response == {"created_at": ["Enter a valid date."]}
