from django.db import models


class MeetupRole(models.Model):
    name = models.CharField(max_length=24)
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

