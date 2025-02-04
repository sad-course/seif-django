from datetime import timedelta
import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"Tag: {self.name}"


class Event(models.Model):
    EVENT_STATUS = (
        ("pending", "Pendente"),
        ("active", "Ativo"),
        ("closed", "Encerrado"),
        ("canceled", "Cancelado"),
    )
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField("Título", max_length=150, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")
    init_date = models.DateTimeField("Início da atividade")
    end_date = models.DateTimeField("Fim da atividade")
    status = models.CharField(max_length=50, choices=EVENT_STATUS, default="pending")
    banner = models.ImageField(upload_to="events/banners/")
    tags = models.ManyToManyField(Tag)


class Activity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField("Título", max_length=150, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")
    init_date = models.DateTimeField("Início da atividade")
    end_date = models.DateTimeField("Fim da atividade")
    instructor = models.CharField("Monitor", max_length=150)

    # activity_type = models.CharField() ou ForeignKey?
    estimated_duration = models.DurationField(default=timedelta(hours=0))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Certificate(models.Model):
    certificate_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
