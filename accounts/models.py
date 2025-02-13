from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Participant(AbstractUser):
    username = models.CharField(verbose_name="username", max_length=150)
    email = models.EmailField(verbose_name="email", unique=True, max_length=170)
    cpf = models.CharField(verbose_name="cpf", max_length=11)
    phone = models.CharField(verbose_name="phone", max_length=16)
    avatar = models.ImageField(upload_to="accounts/users/avatar")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name_plural = "Participantes"

    def __str__(self):
        return self.email


class AcademicIntern(Participant):
    registration_number = models.CharField(verbose_name="registration_number")
    association_type = models.CharField(verbose_name="association_type")

    class Meta:
        verbose_name_plural = "Academicos Internos"
