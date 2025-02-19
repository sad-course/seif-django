# Generated by Django 5.1.3 on 2025-02-17 16:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0002_activity_is_active_event_organizers"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="created_by",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events_managed",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
