from django.db import models

class PersonInMeetup(models.Model):
    person_id = models.IntegerField()
    meetup_id = models.IntegerField()
    meetup_role_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['person_id', 'meetup_id', 'meetup_role_id'])
        ]