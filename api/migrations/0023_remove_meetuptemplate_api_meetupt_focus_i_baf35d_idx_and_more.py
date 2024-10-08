# Generated by Django 4.2.5 on 2024-09-08 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_templatetopic_topic_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='meetuptemplate',
            name='api_meetupt_focus_i_baf35d_idx',
        ),
        migrations.RemoveField(
            model_name='meetuptemplate',
            name='focus',
        ),
        migrations.AddField(
            model_name='meetuptemplate',
            name='max_minutes',
            field=models.IntegerField(default=15),
        ),
        migrations.AddIndex(
            model_name='meetuptemplate',
            index=models.Index(fields=['max_minutes'], name='api_meetupt_max_min_177a8e_idx'),
        ),
    ]
