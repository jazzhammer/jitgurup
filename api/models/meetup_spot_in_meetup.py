from django.db import models
from api.models.meetup_spot import MeetupSpot
from api.models.meetup import Meetup

class MeetupSpotInMeetup(models.Model):
    meetup_spot = models.ForeignKey(MeetupSpot, on_delete=models.DO_NOTHING, default=None)
    meetup = models.ForeignKey(Meetup, on_delete=models.DO_NOTHING, default=None)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'meetup_id', 'meetup_spot_id'])
        ]

    def __str__(self):
        return f"meetup_spot_id[{self.meetup_spot_id}]-meetup_id[{self.meetup_id}]"
