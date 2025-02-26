# Generated by Django 5.1.3 on 2025-02-13 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Ativo"),
        ),
        migrations.AddField(
            model_name="event",
            name="organizers",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
