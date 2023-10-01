from django.db import models

class MeetupSpot(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    spot_type_id = models.IntegerField()
    facility_id = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['name', 'spot_type_id', 'facility_id'], name='meetup_spot_idx')
        ]