import pytest

from core.testing.factories import register

pytestmark = pytest.mark.django_db


@register
def campaign(self, **kwargs):
    return self.mixer.blend("models.Campaign", **kwargs)
