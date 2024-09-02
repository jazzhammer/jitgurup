"""

"""
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'])
        ]

