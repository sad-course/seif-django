from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Participant(AbstractUser):
    username = models.CharField(verbose_name="username", max_length=150)
    email = models.EmailField(verbose_name="email", unique=True, max_length=170)
    cpf = models.CharField(verbose_name="cpf", max_length=11)
    phone = models.CharField(verbose_name="phone", max_length=16)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
