from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=48)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'])
        ]

    def __str__(self):
        return self.name
