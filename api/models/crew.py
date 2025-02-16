from django.db import models
from django.db.models import DO_NOTHING, Index

from api.models.meetup import Meetup


class Crew(models.Model):
    name = models.CharField(max_length=128)
    meetup = models.ForeignKey(Meetup, null=True, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)

    def __repr__(self):
        return f"name[{self.id}]"

    class Meta:
        indexes = [
            Index(fields=['name', 'deleted']),
        ]