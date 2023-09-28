from django.db import models

class Person(models.Model):
    last_name = models.CharField(max_length=48)
    first_name = models.CharField(max_length=48)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'], name='person_idx'),
        ]

class OrgPerson(models.Model):
    org_id = models.IntegerField()
    person_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['org_id', 'person_id'], name='org_person_idx'),
        ]
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

class UserOrg(models.Model):
    user_id = models.IntegerField()
    org_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'org_id'], name='user_org_idx')
        ]

class MeetUp(models.Model):
    start_at = models.DateTimeField()
    duration = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['start_at'])
        ]

class ShowUp(models.Model):
    person_id = models.IntegerField()
    meetup_role_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['person_id', 'meetup_role_id'])
        ]

class MeetupRole(models.Model):
    name = models.CharField(max_length=24)
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

class Profession(models.Model):
    name = models.CharField(max_length=48)
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]