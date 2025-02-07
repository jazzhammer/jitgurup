from django.db.models import Model, DO_NOTHING
from django.db import models

from api.models.meetup_template import MeetupTemplate
from api.models.prereq_set import PrereqSet


class PrereqDetail(Model):
    prereq_set = models.ForeignKey(PrereqSet, on_delete=DO_NOTHING)
    meetup_template = models.ForeignKey(MeetupTemplate, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)
    mandatory = models.BooleanField(default=True)