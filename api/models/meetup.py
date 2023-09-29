from django.db import models


class Meetup(models.Model):
    start_at = models.DateTimeField()
    duration = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['start_at'])
        ]

