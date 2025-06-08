from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.strategies.api.v1.agency.views import StrategyView

router = SimpleRouter()

router.register("", StrategyView)

urlpatterns = [
    path("", include(router.urls)),
]
