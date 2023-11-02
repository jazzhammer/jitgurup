from django.db import models


class Person(models.Model):
    last_name = models.CharField(max_length=48)
    first_name = models.CharField(max_length=48)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'last_name', 'first_name'], name='person_idx'),
        ]

    def __str__(self):
        return f"{self.last_name.upper()}, {self.first_name.lower()}"

