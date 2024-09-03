"""

"""
from django.db import models
from django.db.models import DO_NOTHING

from api.models.subject import Subject


class Topic(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=DO_NOTHING)
    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name']),
            models.Index(fields=['deleted', 'subject_id']),
        ]

