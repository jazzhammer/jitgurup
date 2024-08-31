from django.db import models

class Tool(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)