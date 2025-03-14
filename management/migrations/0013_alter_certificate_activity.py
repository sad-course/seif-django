# Generated by Django 5.1.3 on 2025-02-21 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0012_alter_event_campus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificate",
            name="activity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="activities",
                to="management.activity",
            ),
        ),
    ]
