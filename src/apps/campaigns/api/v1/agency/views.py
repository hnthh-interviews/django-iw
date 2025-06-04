from apps.campaigns.api.v1.agency.serializers import CampaignListAsAgencySerializer
from core.api.views import AppGenericViewSet, AppListModelMixin
from models.models import Campaign


class CampaignView(AppListModelMixin, AppGenericViewSet):
    http_method_names = ("get",)
    queryset = Campaign.objects.all()
    serializer_action_classes = {
        "list": CampaignListAsAgencySerializer,
    }
    serializer_class = CampaignListAsAgencySerializer
