from django.contrib import admin
from django.urls import include, path

agency = [
    path("campaigns/", include("apps.campaigns.api.v1.agency.urls")),
]

urlpatterns = [
    path("api/v1/agency/", include(agency)),
    path("admin/", admin.site.urls),
]
