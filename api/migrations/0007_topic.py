# Generated by Django 4.2.5 on 2024-09-03 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('deleted', models.BooleanField(default=False)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.subject')),
            ],
            options={
                'indexes': [models.Index(fields=['deleted', 'name'], name='api_topic_deleted_b7e4aa_idx'), models.Index(fields=['deleted', 'subject_id'], name='api_topic_deleted_bb2506_idx')],
            },
        ),
    ]