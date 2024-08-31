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

    def save(self, *args, **kwargs):
        self.last_name = self.last_name.lower()
        self.first_name = self.first_name.lower()
        super(Person, self).save(*args, **kwargs)