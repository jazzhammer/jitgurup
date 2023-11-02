from django.contrib.auth.models import User
from django.db import models

# a user is 0 - n persons in the real world
# eg.   at org='bethlehem school for the young and brainwashed", a user is bob, but also:
#       at org='falkland elementary", a user is charlie
from api.models.person import Person


class UserPerson(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'user_id', 'person_id'], name='user_person_idx')
        ]
    def __str(self):
        return f"user[{self.user_id}]-person[{self.person_id}]"
