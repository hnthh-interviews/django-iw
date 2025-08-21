from django_filters import DateTimeFilter, FilterSet

from models.models import Campaign


class CampaignFilter(FilterSet):
    created_after = DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Кампании, созданные после даты (YYYY-MM-DD)",
    )
    created_before = DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Кампании, созданные до даты (YYYY-MM-DD)",
    )

    class Meta:
        model = Campaign
        fields = ["created_after", "created_before"]
