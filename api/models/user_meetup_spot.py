from django.db import models


# captures assignment of a meetup_spot with a user that frequently interacts with it.
# allows rendering a list of user's most frequented meetup_spots
class UserMeetupSpot(models.Model):
    user_id = models.IntegerField()
    meetup_spot_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'meetup_spot_id'], name='user_meetup_spot_idx')
        ]
