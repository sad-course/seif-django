from django.db import models
from accounts.models import Participant
from management.models import Event, Activity


# Create your models here.
class EventSubscription(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    activity = models.ForeignKey(
        to=Activity, on_delete=models.CASCADE, related_name="subscriptions"
    )
