# Generated by Django 4.2.5 on 2023-09-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_facility"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="facility",
            name="facility_idx",
        ),
        migrations.AddField(
            model_name="facility",
            name="org_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="facility",
            index=models.Index(fields=["name", "org_id"], name="facility_idx"),
        ),
    ]