from django.db import models

class Village(models.Model):
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(null=False)
    deleted = models.BooleanField(default=False)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['description']),
            models.Index(fields=['deleted'])
        ]