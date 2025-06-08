import pytest

from core.testing.factories import register

pytestmark = pytest.mark.django_db


@register
def strategy(self, **kwargs):
    return self.mixer.blend("models.Strategy", **kwargs)
