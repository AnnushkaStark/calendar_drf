# Generated by Django 5.1 on 2024-08-27 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EventModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("start_time", models.DateTimeField()),
                ("period", models.IntegerField(blank=True, null=True)),
                ("reccurence_limit", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
