from django.db import models


class SpotType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='org_idx'),
        ]

