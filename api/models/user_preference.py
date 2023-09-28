from django.db.models import *
from django.db import models


class UserPreference(Model):
    user_id = IntegerField()
    name = CharField(max_length=32)
    value = CharField(max_length=32)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'name'], name='user_preference_idx')
        ]
