from apps.strategies.api.v1.agency.serializers import StrategyListAsAgencySerializer
from core.api.views import AppGenericViewSet, AppListModelMixin
from models.models import Strategy


class StrategyView(AppListModelMixin, AppGenericViewSet):
    http_method_names = ("get",)
    queryset = Strategy.objects.select_related("campaign").order_by("name")
    serializer_action_classes = {
        "list": StrategyListAsAgencySerializer,
    }
    serializer_class = StrategyListAsAgencySerializer
