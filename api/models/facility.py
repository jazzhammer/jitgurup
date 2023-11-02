from django.db import models
from django.db.models import *

from api.models.org import Org


class Facility(models.Model):
    name = CharField(max_length=64)
    description = TextField()
    org = models.ForeignKey(Org, on_delete=models.DO_NOTHING)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'org_id', 'deleted'], name='facility_idx'),
        ]

    def __str__(self):
        return self.name
