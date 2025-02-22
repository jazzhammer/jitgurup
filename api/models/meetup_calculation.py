from django.db import models
from django.db.models import DO_NOTHING

from api.models.facility import Facility
from api.models.org import Org
from api.models.village import Village


class MeetupCalculation(models.Model):
    pupil_count = models.IntegerField(default=0)
    guru_count = models.IntegerField(default=0)
    daily_meetup_interval_length = models.IntegerField(default=0)
    intermeetup_transition = models.IntegerField(default=0)
    max_meetups_per_guru_per_day = models.IntegerField(default=0)
    total_guru_minutes_per_day = models.IntegerField(default=0)
    max_pupil_meetups_per_day = models.IntegerField(default=0)
    minimum_pupil_meetups_per_day = models.IntegerField(default=0)
    org = models.ForeignKey(Org, null=True, on_delete=DO_NOTHING)
    facility = models.ForeignKey(Facility, null=True, on_delete=DO_NOTHING)
    village = models.ForeignKey(Village, null=True, on_delete=DO_NOTHING)
