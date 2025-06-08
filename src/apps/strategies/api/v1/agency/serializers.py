from rest_framework import serializers

from apps.campaigns.api.v1.agency.serializers import CampaignListAsAgencySerializer
from models.models import Strategy


class StrategyListAsAgencySerializer(serializers.ModelSerializer):
    campaign = CampaignListAsAgencySerializer(read_only=True)

    class Meta:
        model = Strategy
        fields = (
            "id",
            "campaign",
            "name",
        )
