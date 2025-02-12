import uuid
from django.db import models
from accounts.models import Participant
from management.models import Event, Activity


# Create your models here.
class EventSubscritption(models.Model):
    event_subcription_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    activities = models.ManyToManyField(Activity)
