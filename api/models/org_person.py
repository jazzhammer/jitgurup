from django.db import models


class OrgPerson(models.Model):
    org_id = models.IntegerField()
    person_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['org_id', 'person_id'], name='org_person_idx'),
        ]
