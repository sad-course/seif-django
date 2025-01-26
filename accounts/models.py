from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(models.Model):
    name = models.CharField(verbose_name="name", max_length=40)
    email = models.EmailField(verbose_name="email", unique=True)
    password = models.CharField(verbose_name="password", max_length=16)
    phone = models.CharField(verbose_name="phone", max_length=14)
    cpf = models.CharField(verbose_name="cpf", max_length=16)


class Teste(AbstractUser):
    username = models.CharField(max_length=10, blank=True, null=True, unique=True)
    email = models.EmailField(verbose_name="email", unique=True)
    cpf = models.CharField(max_length=16)
    phone = models.CharField(max_length=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email
