# Generated by Django 5.1.3 on 2025-02-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0018_alter_event_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="observation",
            field=models.TextField(blank=True, null=True, verbose_name="Observação"),
        ),
    ]
