from django.db import models
from django.db.models import Model, DO_NOTHING, CASCADE

from api.models.meetup_template import MeetupTemplate


class PrereqSet(Model):
    # required_by = models.ForeignKey(MeetupTemplate, on_delete=DO_NOTHING)
    meetup_template = models.ForeignKey(MeetupTemplate, on_delete=DO_NOTHING)
    """
    indicates how many prereqs out of the set of prereqs are mandatory 
    """
    rule_numerator = models.IntegerField(default=1)
    deleted = models.BooleanField(default=False)