from django.db import models
from django.db.models import DO_NOTHING

"""
has n template_roles 

defines a combination (of roles) that is instantiable and each instance is assignable to a meetup.
meetup-template -> crew-template -> template-roles
when instantiated:
meetup -> crew -> roles 

"""
class CrewTemplate(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'deleted']),
        ]