from django_filters.rest_framework import DjangoFilterBackend

from apps.campaigns.api.v1.agency.filters import CampaignFilter
from apps.campaigns.api.v1.agency.serializers import CampaignListAsAgencySerializer
from core.api.views import AppGenericViewSet, AppListModelMixin
from models.models import Campaign


class CampaignView(AppListModelMixin, AppGenericViewSet):
    http_method_names = ("get",)
    queryset = Campaign.objects.order_by("name")
    serializer_action_classes = {
        "list": CampaignListAsAgencySerializer,
    }
    serializer_class = CampaignListAsAgencySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CampaignFilter
