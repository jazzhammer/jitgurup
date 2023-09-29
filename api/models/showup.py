from django.db import models


class Showup(models.Model):
    person_id = models.IntegerField()
    meetup_role_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['person_id', 'meetup_role_id'])
        ]

