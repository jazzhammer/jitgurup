# Generated by Django 4.2.5 on 2024-09-06 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_meetuptemplate_facility_meetuptemplate_meetup_spot_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('deleted', models.BooleanField(default=False)),
                ('crew_template', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.crewtemplate')),
            ],
            options={
                'indexes': [models.Index(fields=['name', 'deleted'], name='api_crew_name_acfd8d_idx'), models.Index(fields=['crew_template_id', 'deleted'], name='api_crew_crew_te_e805aa_idx'), models.Index(fields=['name', 'crew_template_id', 'deleted'], name='api_crew_name_9c1607_idx')],
            },
        ),
    ]