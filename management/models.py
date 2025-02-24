import uuid
from datetime import timedelta

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import Participant


# Create your models here.
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"Tag: {self.name}"


class ActivityType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")


class Event(models.Model):
    class EventStatus(models.TextChoices):  # pylint: disable=too-many-ancestors
        PENDING = "pending", "Pendente"
        ACTIVE = "active", "Ativo"
        CLOSED = "closed", "Encerrado"
        CANCELED = (
            "canceled",
            "Cancelado",
        )
        DRAFT = "draft", "Não aprovado"
        APPROVED = "approved", "Aprovado"
        RECUSED = "recused", "Recusado"

    class Campus(models.TextChoices):  # pylint: disable=too-many-ancestors
        CAMPUS_NULL = "null", "Null"
        APODI = "AP", "Apodi"
        CAICO = "CA", "Caicó"
        CANGUARETAMA = "CG", "Canguaretama"
        CEARA_MIRIM = "CM", "Ceará-Mirim"
        CURRAIS_NOVOS = "CN", "Currais Novos"
        IPANGUACU = "IP", "Ipanguaçu"
        JOAO_CAMARA = "JC", "João Câmara"
        JUCURUTU = "JU", "Jucurutu"
        LAJES = "LA", "Lajes"
        MACAU = "MA", "Macau"
        MOSSORO = "MO", "Mossoró"
        NATAL_CENTRAL = "NC", "Natal - Central"
        NATAL_CIDADE_ALTA = "NCA", "Natal - Cidade Alta"
        NATAL_ZONA_LESTE = "NZL", "Natal - Zona Leste"
        NATAL_ZONA_NORTE = "NZN", "Natal - Zona Norte"
        NOVA_CRUZ = "NV", "Nova Cruz"
        PARELHAS = "PA", "Parelhas"
        PARNAMIRIM = "PM", "Parnamirim"
        PAU_DOS_FERROS = "PF", "Pau dos Ferros"
        SANTA_CRUZ = "SC", "Santa Cruz"
        SAO_GONCALO_DO_AMARANTE = "SG", "São Gonçalo do Amarante"
        SAO_PAULO_DO_POTENGI = "SP", "São Paulo do Potengi"

    title = models.CharField("Título", max_length=150, blank=False, null=False)
    description = CKEditor5Field("Descrição", config_name="extends")
    init_date = models.DateTimeField("Início da atividade")
    end_date = models.DateTimeField("Fim da atividade")
    campus = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=Campus.choices,
        default=Campus.CAMPUS_NULL,
    )
    status = models.CharField(
        "", max_length=50, choices=EventStatus.choices, default=EventStatus.DRAFT
    )
    banner = models.ImageField(
        "Banner",
        upload_to="events/banners/",
        default="events/banners/event-banner-default.jpg",
    )
    tags = models.ManyToManyField(to=Tag, verbose_name="Tags")
    organizers = models.ManyToManyField(to=Participant, verbose_name="Organizadores")
    created_by = models.ForeignKey(
        to=Participant,
        on_delete=models.CASCADE,
        related_name="events_managed",
        verbose_name="Criado por",
    )
    observation = models.TextField(blank=True, null=True, verbose_name="Observação")

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
    capacity = models.IntegerField(verbose_name="Capacidade", default=0)
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.SET_NULL,
        verbose_name="Tipo",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Atividades"

    def __str__(self):
        return f"Atividade: {self.title}"


class Certificate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    participant = models.ForeignKey(to=Participant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"Certificado: {self.activity.title}"
