from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.campaigns.api.v1.agency.views import CampaignView

router = SimpleRouter()

router.register("", CampaignView)

urlpatterns = [
    path("", include(router.urls)),
]
