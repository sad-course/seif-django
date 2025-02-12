import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from management.models import Event


# Create your models here.
class Participant(AbstractUser):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(verbose_name="username", max_length=150)
    email = models.EmailField(verbose_name="email", unique=True, max_length=170)
    cpf = models.CharField(verbose_name="cpf", max_length=11)
    phone = models.CharField(verbose_name="phone", max_length=16)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name_plural = "Participantes"

    def __str__(self):
        return self.email


class Organizer(Participant):
    organizer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    events_managed = models.ManyToManyField(
        Event, related_name="organizer", verbose_name="Eventos gerenciados"
    )

    class Meta:
        verbose_name_plural = "Organizadores"


class Administrator(Participant):
    administrator_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        verbose_name_plural = "Administradores"


class AcademicIntern(Participant):
    suap_intern_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    registration_number = models.CharField(verbose_name="registration_number")
    association_type = models.CharField(verbose_name="association_type")

    class Meta:
        verbose_name_plural = "Academicos Internos"
