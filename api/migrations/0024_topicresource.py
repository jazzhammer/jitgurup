# Generated by Django 4.2.5 on 2024-09-09 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_remove_meetuptemplate_api_meetupt_focus_i_baf35d_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('url', models.URLField(max_length=128)),
                ('deleted', models.BooleanField(default=False)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.topic')),
            ],
            options={
                'indexes': [models.Index(fields=['deleted', 'description'], name='api_topicre_deleted_e96700_idx'), models.Index(fields=['deleted', 'topic_id'], name='api_topicre_deleted_f51f99_idx'), models.Index(fields=['deleted', 'topic_id', 'description'], name='api_topicre_deleted_41f886_idx')],
            },
        ),
    ]