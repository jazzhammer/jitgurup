"""
'what do you want to get out of a meetup ? '
the answer to this question is the focus.
eg.
a pupil could attend a meetup for subject: woodworking, topic: glue-ups
the default focus would be to 'learn glue-up techniques'
if the focus is something other than the default,
the focus will probably have something to do with glue-ups, eg. 'learn types of glue used in glue-ups'
"""
from django.db import models

class Focus(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'])
        ]

