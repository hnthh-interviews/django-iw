from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Manager, Model
from django.utils import timezone


class AppManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class AppModelMixin:
    def refresh(self, **kwargs):
        self.refresh_from_db(**kwargs)

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.save()

        return self


class AppModel(Model, AppModelMixin):
    objects = Manager()

    class Meta:
        abstract = True


class TimestampedModel(AppModel):
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified_at = timezone.now()

        return super().save(*args, **kwargs)
