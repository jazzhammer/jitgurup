from django.db import models


class SpotType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'], name='spot_type_idx'),
        ]

    def __str__(self):
        return self.name
