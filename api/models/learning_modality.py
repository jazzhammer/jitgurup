from django.db import models

class LearningModality(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'deleted'])
        ]