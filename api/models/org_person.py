from django.db import models

from api.models.person import Person
from api.models.org import Org


class OrgPerson(models.Model):
    org = models.ForeignKey(Org, default=None, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'org_id', 'person_id'], name='org_person_idx'),
        ]

    def __str__(self):
        return f"org_id[{self.org_id}]-person_id[{self.person_id}]"

