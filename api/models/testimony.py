from django.db import models

class Testimony(models.Model):
    content = models.TextField(null=False, blank=False)
    type = models.CharField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'type'])
        ]

