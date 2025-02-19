# Generated by Django 5.1.3 on 2025-02-19 09:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_populate_attendance_indentifier_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventsubscription",
            name="attendance_indentifier",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        )
    ]
