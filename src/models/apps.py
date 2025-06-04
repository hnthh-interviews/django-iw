from django.apps import AppConfig
from django.conf import settings


class ModelsConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = "models"
