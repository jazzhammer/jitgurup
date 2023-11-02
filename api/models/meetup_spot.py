from django.db import models
from api.models.spot_type import SpotType
from api.models.facility import Facility

class MeetupSpot(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    spot_type = models.ForeignKey(SpotType, on_delete=models.DO_NOTHING, default=None)
    facility = models.ForeignKey(Facility, on_delete=models.DO_NOTHING, default=None)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name', 'spot_type_id', 'facility_id'], name='meetup_spot_idx')
        ]

    def __str__(self):
        return self.name