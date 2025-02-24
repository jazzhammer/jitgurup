from django.db import models
from django.db.models import *

class FrequentQuestion(models.Model):
    content = TextField()
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted']),
        ]
