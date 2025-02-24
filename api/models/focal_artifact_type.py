from django.db import models
from django.db.models import *

class FocalArtifactType(models.Model):
    name = CharField(max_length=64)
    description = TextField()
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'deleted']),
        ]

    def __str__(self):
        return self.name
