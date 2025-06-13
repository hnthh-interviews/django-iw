from rest_framework import serializers

from apps.strategies.api.v1.agency.serializers.campaign import CampaignForStrategyListSerializer
from models.models import Strategy


class StrategyListAsAgencySerializer(serializers.ModelSerializer):
    campaign = CampaignForStrategyListSerializer(read_only=True)

    class Meta:
        model = Strategy
        fields = (
            "campaign",
            "id",
            "name",
        )
