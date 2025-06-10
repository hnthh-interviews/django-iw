from core.models import TimestampedModel, models
from models.models.campaign import Campaign


class Strategy(TimestampedModel):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)

    class Meta:
        default_related_name = "strategies"
