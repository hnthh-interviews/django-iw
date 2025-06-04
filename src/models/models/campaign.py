from core.models import TimestampedModel, models


class Campaign(TimestampedModel):
    name = models.CharField(max_length=1024)

    class Meta:
        default_related_name = "campaigns"
