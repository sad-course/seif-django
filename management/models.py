from datetime import timedelta
import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import Participant


# Create your models here.
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"Tag: {self.name}"


class Event(models.Model):
    class EventStatus(models.TextChoices):  # pylint: disable=too-many-ancestors
        PENDING = "pending", "Pendente"
        ACTIVE = "active", "Ativo"
        CLOSED = "closed", "Encerrado"
        CANCELED = (
            "canceled",
            "Cancelado",
        )
        DRAFT = "draft", "Rascunho"
        APPROVED = "approved", "Aprovado"

    title = models.CharField("Título", max_length=150, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")
    init_date = models.DateTimeField("Início da atividade")
    end_date = models.DateTimeField("Fim da atividade")
    campus = models.CharField(max_length=50, blank=False, null=False)
    status = models.CharField(
        "", max_length=50, choices=EventStatus.choices, default=EventStatus.DRAFT
    )
    banner = models.ImageField(
        "Banner",
        upload_to="events/banners/",
        default="/static/images/event-banner-default.png",
    )
    tags = models.ManyToManyField(to=Tag, verbose_name="Tags")
    organizers = models.ManyToManyField(to=Participant, verbose_name="Organizadores")
    created_by = models.ForeignKey(
        to=Participant,
        on_delete=models.CASCADE,
        related_name="events_managed",
        verbose_name="Criado por",
    )

    class Meta:
        verbose_name_plural = "Eventos"

    def __str__(self):
        return f"Evento: {self.title}"


class Activity(models.Model):
    title = models.CharField("Título", max_length=150, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")
    init_date = models.DateTimeField("Início da atividade")
    end_date = models.DateTimeField("Fim da atividade")
    instructor = models.CharField("Monitor", max_length=150)
    estimated_duration = models.DurationField(default=timedelta(hours=0))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Evento")
    is_active = models.BooleanField(verbose_name="Ativo", default=True)

    class Meta:
        verbose_name_plural = "Atividades"

    def __str__(self):
        return f"Atividade: {self.title}"


class Certificate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"Certificado: {self.activity.title}"
