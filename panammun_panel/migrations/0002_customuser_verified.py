# Generated by Django 5.1 on 2024-08-19 03:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("panammun_panel", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]