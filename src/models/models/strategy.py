from core.models import TimestampedModel, models
from models.models.campaign import Campaign


class Strategy(TimestampedModel):
    name = models.CharField(max_length=1024)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "strategies"
