from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Participant(AbstractUser):
    username = models.CharField(verbose_name="Nome de usuário", max_length=150)
    email = models.EmailField(verbose_name="E-mail", unique=True, max_length=170)
    cpf = models.CharField(verbose_name="CPF", max_length=11)
    phone = models.CharField(verbose_name="Telefone", max_length=16)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
