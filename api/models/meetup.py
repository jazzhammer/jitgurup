from django.db import models
from django.db.models import DO_NOTHING

from api.models.crew import Crew
from api.models.facility import Facility
from api.models.meetup_spot import MeetupSpot
from api.models.meetup_template import MeetupTemplate
from api.models.org import Org


class Meetup(models.Model):
    start_at = models.DateTimeField()
    # in minutes
    duration = models.IntegerField()

    # at least copied from the meetup template
    # likely modified by the guru hosting the meetup
    name = models.CharField(max_length=64)

    # for larger organizations and more complex learning environments,
    # these fields will likely be filled.
    # by default, they should be optional
    meetup_template = models.ForeignKey(MeetupTemplate, null=True, on_delete=DO_NOTHING)
    org = models.ForeignKey(Org, null=True, on_delete=DO_NOTHING)
    facility = models.ForeignKey(Facility, null=True, on_delete=DO_NOTHING)
    meetup_spot = models.ForeignKey(MeetupSpot, null=True, on_delete=DO_NOTHING)
    crew = models.ForeignKey(Crew, null=True, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'start_at', 'name'])
        ]

    def __str__(self):
        return self.name

