from django.db import models

class CrewTemplate(models.Model):

    name = models.CharField(max_length=128)
