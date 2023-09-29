from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=48)
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]