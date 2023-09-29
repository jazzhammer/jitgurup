from django.db import models

# a user is 0 - n persons in the real world
# eg.   at org='bethlehem school for the young and brainwashed", a user is bob, but also:
#       at org='falkland elementary", a user is charlie
class UserPerson(models.Model):
    user_id = models.IntegerField()
    person_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'person_id'], name='user_person_idx')
        ]
