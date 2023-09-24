from django.db import models

class Person(models.Model):
    last_name = models.CharField(max_length=48)
    first_name = models.CharField(max_length=48)

class MeetUp(models.Model):
    start_at = models.DateTimeField()
    duration = models.IntegerField()

class ShowUp(models.Model):
    person_id = models.IntegerField()
    meetup_role_id = models.IntegerField()

class MeetupRole(models.Model):
    name = models.CharField(max_length=24)

class Profession(models.Model):
    name = models.CharField(max_length=48)
