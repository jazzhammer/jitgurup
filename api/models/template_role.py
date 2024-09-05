from django.db import models
from django.db.models import *

from api.models.crew_template import CrewTemplate


class TemplateRole(models.Model):
    name = CharField(max_length=64)
    description = TextField()
    crew_template = models.ForeignKey(CrewTemplate, on_delete=models.DO_NOTHING)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['crew_template_id', 'deleted']),
            models.Index(fields=['name', 'deleted']),
        ]

    def __str__(self):
        return self.name
