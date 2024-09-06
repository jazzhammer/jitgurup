from django.db import models
from django.db.models import DO_NOTHING, Index

from api.models.crew_template import CrewTemplate


class Crew(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)
    crew_template = models.ForeignKey(CrewTemplate, on_delete=DO_NOTHING)

    class Meta:
        indexes = [
            Index(fields=['name', 'deleted']),
            Index(fields=['crew_template_id', 'deleted']),
            Index(fields=['name', 'crew_template_id', 'deleted'])
        ]