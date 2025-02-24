from django.db import models
from django.db.models import *

from api.models.frequent_question import FrequentQuestion


class FrequentAnswer(models.Model):
    content = TextField()
    frequent_question = models.ForeignKey(FrequentQuestion, on_delete=models.DO_NOTHING)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted']),
        ]
