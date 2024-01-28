# Generated by Django 5.0.1 on 2024-01-28 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calendar", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="date",
        ),
        migrations.AddField(
            model_name="event",
            name="end",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="start",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
