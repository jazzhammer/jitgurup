from django.db import models

class MeetupSpotInMeetup(models.Model):
    meetup_spot_id = models.IntegerField()
    meetup_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['person_id', 'meetup_spot_id'])
        ]