from django.db import models
from django.db.models import DO_NOTHING

from api.models.crew_template import CrewTemplate
from api.models.facility import Facility
from api.models.focus import Focus
from api.models.meetup_spot import MeetupSpot
from api.models.org import Org
from api.models.subject import Subject
from api.models.topic import Topic


class MeetupTemplate(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)
    # the same crew needs to meetup multiple times
    # each time, the work in progress is advanced until complete
    work_in_progress = models.BooleanField(default=False)
    org = models.ForeignKey(Org, null=True, on_delete=DO_NOTHING)
    facility = models.ForeignKey(Facility, null=True, on_delete=DO_NOTHING)
    meetup_spot= models.ForeignKey(MeetupSpot, null=True, on_delete=DO_NOTHING)
    crew_template = models.ForeignKey(CrewTemplate, null=True, on_delete=DO_NOTHING)
    focus = models.ForeignKey(Focus, null=True, on_delete=DO_NOTHING)
    subject = models.ForeignKey(Subject, null=True, on_delete=DO_NOTHING)
    topic = models.ForeignKey(Topic, null=True, on_delete=DO_NOTHING)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['crew_template_id']),
            models.Index(fields=['focus_id']),
            models.Index(fields=['subject_id']),
            models.Index(fields=['topic_id']),
            models.Index(fields=['deleted']),
            models.Index(fields=['work_in_progress'])
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(MeetupTemplate, self).save(*args, **kwargs)