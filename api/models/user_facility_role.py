from django.db import models
from django.db.models import *

class UserFacilityRole(models.Model):
    user_id = IntegerField()
    facility_id = IntegerField()
    role_id = IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'facility_id', 'role_id'], name='user_facility_role_idx')
        ]