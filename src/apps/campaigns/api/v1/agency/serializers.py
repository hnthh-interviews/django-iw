from rest_framework import serializers

from models.models import Campaign


class CampaignListAsAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "id",
            "name",
        )
