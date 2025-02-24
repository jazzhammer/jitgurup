"""
'what do you want to get out of a meetup ? '
the answer to this question is the focus.
eg.
a pupil could attend a meetup for subject: woodworking, topic: glue-ups
the default focus would be to 'learn glue-up techniques'
if the focus is something other than the default,
the focus will probably have something to do with glue-ups, eg. 'learn types of glue used in glue-ups'

eg.
a guru could attend a meetup for subject: woodworking, topic: glue-ups
the default focus would be to 'teach glue-up techniques'
if the focus is something other than the default,
the focus will probably have something to do with glue-ups, eg. 'teach types of glue used in glue-ups'
"""
from django.db import models
from django.db.models import DO_NOTHING

from api.models.topic import Topic


class Focus(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=False)
    topic = models.ForeignKey(Topic, null=True, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'])
        ]

