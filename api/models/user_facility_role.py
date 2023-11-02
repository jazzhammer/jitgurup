from django.contrib.auth.models import User
from django.db import models
from django.db.models import *

from api.models.meetup_role import MeetupRole
from api.models.facility import Facility




class UserFacilityRole(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    facility = models.ForeignKey(Facility, default=None, on_delete=models.DO_NOTHING)
    meetup_role = models.ForeignKey(MeetupRole, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'user_id', 'facility_id', 'role_id'], name='user_facility_role_idx')
        ]

    def __str__(self):
        return f"user[{self.user_id}]-facility[{self.facility_id}]-role[{self.role_id}]"

