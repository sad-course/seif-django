# Generated by Django 5.1.3 on 2025-02-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0005_alter_event_banner_alter_event_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="campus",
            field=models.CharField(default="", max_length=50),
            preserve_default=False,
        ),
    ]
