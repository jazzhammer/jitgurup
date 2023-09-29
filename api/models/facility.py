from django.db import models
from django.db.models import *


class Facility(models.Model):
    name = CharField(max_length=64)
    description = TextField()
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='facility_idx'),
        ]