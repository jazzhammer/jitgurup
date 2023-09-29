from django.db import models
from django.db.models import *


class Facility(models.Model):
    org_id = IntegerField()
    name = CharField(max_length=64)
    description = TextField()
    class Meta:
        indexes = [
            models.Index(fields=['name', 'org_id'], name='facility_idx'),
        ]