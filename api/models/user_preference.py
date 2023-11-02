from django.contrib.auth.models import User
from django.db.models import *
from django.db import models


class UserPreference(Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    name = CharField(max_length=32)
    value = CharField(max_length=32)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'user_id', 'name'], name='user_preference_idx')
        ]

    def __str__(self):
        return self.name