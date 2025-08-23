from django_filters import rest_framework as filters

from models.models import Campaign


class CampaignFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Campaign
        fields = ["created_at"]
