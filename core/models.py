from django.db import models
from accounts.models import Participant
from management.models import Event, Activity


# Create your models here.
class EventSubscritption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    activities = models.ManyToManyField(Activity)
