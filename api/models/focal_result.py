from django.db import models
from django.db.models import *
from api.models.signup import Signup

"""
could be anything that comes out of the attendance of a guru or pupil in a meetup.
"""
class FocalResult(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.DO_NOTHING)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted']),
        ]
