from django.db import models


class Meetup(models.Model):
    start_at = models.DateTimeField()
    # as minutes
    duration = models.IntegerField()
    name = models.CharField(max_length=64)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'start_at', 'name'])
        ]

    def __str__(self):
        return self.name

