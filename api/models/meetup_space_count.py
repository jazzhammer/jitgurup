from django.db import models
from django.db.models import *

from api.models.meetup_calculation import MeetupCalculation


class MeetupSpaceCount(models.Model):
    max_persons = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    meetup_calculation = models.ForeignKey(MeetupCalculation, on_delete=DO_NOTHING)
    deleted = BooleanField(default=False)

