from django.db import models

GURU = 'guru'
PUPIL = 'pupil'
OBSERVER = 'observer'

class MeetupRole(models.Model):
    name = models.CharField(max_length=24)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'])
        ]

    def __str__(self):
        return self.name

