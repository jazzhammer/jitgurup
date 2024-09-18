"""

"""
from django.db import models
from django.db.models import DO_NOTHING

from api.models.topic import Topic


class TopicResource(models.Model):
    description = models.TextField()
    url = models.URLField(max_length=128)
    topic = models.ForeignKey(Topic, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'description']),
            models.Index(fields=['deleted', 'topic_id']),
            models.Index(fields=['deleted', 'topic_id', 'description'])
        ]

