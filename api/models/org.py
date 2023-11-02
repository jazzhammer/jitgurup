from django.db import models

class Org(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'], name='org_idx'),
        ]

    def __str__(self):
        return self.name

