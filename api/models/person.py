from django.db import models


class Person(models.Model):
    last_name = models.CharField(max_length=48)
    first_name = models.CharField(max_length=48)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'], name='person_idx'),
        ]

