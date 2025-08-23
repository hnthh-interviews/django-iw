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
    for i, date in enumerate(dates):
        with freeze_time(date):
            campaigns.append(factory.campaign(name=f"campaign{i}"))
    return campaigns


@pytest.mark.parametrize(
    ("filter_option", "expected_campaign_id"),
    [
        ({"created_at_after": "2025-08-20"}, [2, 3]),
        ({"created_at_before": "2025-08-20"}, [1, 2]),
        ({"created_at_before": "2025-08-18", "created_at_after": "2025-08-22"}, []),
    ],
)
def test_filter_by_date(as_anon, url, filter_option, expected_campaign_id):
    response = as_anon.get(url, filter_option)
    results = [x["id"] for x in response["results"]]

    assert response.status == HTTPStatus.OK
    assert results == expected_campaign_id
