# Generated by Django 4.2.2 on 2023-10-01 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_userperson_showup_profession_orgperson_meetuprole_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpotType",
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
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
            ],
            options={
                "indexes": [models.Index(fields=["name"], name="spot_type_idx")],
            },
        ),
        migrations.CreateModel(
            name="MeetupSpot",
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
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("spot_type_id", models.IntegerField()),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["name", "spot_type_id"], name="meetup_spot_idx"
                    )
                ],
            },
        ),
    ]