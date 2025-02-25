import uuid
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
    is_subcription_canceled = models.BooleanField(default=False)
    attendance_indentifier = models.UUIDField(unique=True, default=uuid.uuid4)
    is_checked_in = models.BooleanField(default=False)
    check_in_qr_code = models.ImageField(
        upload_to="checkin/qrcode/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Inscrições em Evento"

    def __str__(self):
        return f"Event={self.event.title}:Activity={self.activity.title}"
