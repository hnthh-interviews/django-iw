from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

agency = [
    path("campaigns/", include("apps.campaigns.api.v1.agency.urls")),
    path("strategies/", include("apps.strategies.api.v1.agency.urls")),
]

urlpatterns = [
    path("api/v1/agency/", include(agency)),
    path("admin/", admin.site.urls),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
