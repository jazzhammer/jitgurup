from django.db import models
from django.db.models import DO_NOTHING, Index

from api.models.meetup_template import MeetupTemplate
from api.models.topic import Topic


class TemplateTopic(models.Model):
    meetup_template = models.ForeignKey(MeetupTemplate, on_delete=DO_NOTHING)
    topic = models.ForeignKey(Topic, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            Index(fields=['meetup_template_id', 'deleted']),
            Index(fields=['topic_id', 'deleted']),
            Index(fields=['meetup_template_id', 'topic_id', 'deleted']),
            Index(fields=['topic_id']),
            Index(fields=['meetup_template_id']),
        ]