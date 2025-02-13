from django.contrib.auth.models import User
from django.db import models
from django.db.models import DO_NOTHING, Index

from api.models.crew import Crew
from api.models.meetup_role import MeetupRole
from api.models.person import Person


class Signup(models.Model):
    person = models.ForeignKey(Person, on_delete=DO_NOTHING)
    crew = models.ForeignKey(Crew, null=True, on_delete=DO_NOTHING)
    meetup_role = models.ForeignKey(MeetupRole, null=True, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=DO_NOTHING)
    class Meta:
        indexes = [
            Index(fields=['person_id']),
            Index(fields=['crew_id']),
            Index(fields=['meetup_role_id']),
            Index(fields=['created_at']),
            Index(fields=['deleted']),
            Index(fields=['created_by']),
        ]