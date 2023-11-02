from django.db import models

from api.models.person import Person
from api.models.meetup import Meetup
from api.models.meetup_role import MeetupRole

class PersonInMeetup(models.Model):
    person = models.ForeignKey(Person, default=None, on_delete=models.DO_NOTHING)
    meetup = models.ForeignKey(Meetup, default=None, on_delete=models.DO_NOTHING)
    meetup_role = models.ForeignKey(MeetupRole, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'person_id', 'meetup_id', 'meetup_role_id'])
        ]

    def __str__(self):
        return f"person[{self.person_id}]-meetup[{self.meetup_id}]-role[{self.meetup_role_id}]"
