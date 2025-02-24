from django.db import models
from django.db.models import *

from api.models.focal_artifact_type import FocalArtifactType
from api.models.focal_result import FocalResult


class FocalArtifact(models.Model):
    name = CharField(max_length=64)
    description = TextField()
    focal_artifact_type = models.ForeignKey(FocalArtifactType, on_delete=models.DO_NOTHING)
    focal_result = models.ForeignKey(FocalResult, on_delete=models.DO_NOTHING)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'deleted']),
        ]

    def __str__(self):
        return self.name
