from django.contrib.auth.models import User
from django.db import models


# captures assignment of a meetup_spot with a user that frequently interacts with it.
# allows rendering a list of user's most frequented meetup_spots
from api.models.meetup_spot import MeetupSpot


class UserMeetupSpot(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    meetup_spot = models.ForeignKey(MeetupSpot, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'user_id', 'meetup_spot_id'], name='user_meetup_spot_idx')
        ]

    def __str__(self):
        return f"user[{self.user_id}]-meetup_spot[{self.meetup_spot_id}]"
