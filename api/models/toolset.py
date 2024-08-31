from django.contrib.auth.models import User
from django.db.models import Model, DO_NOTHING
from django.db import models

from api.models.tool import Tool


class Toolset(Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    deleted = models.BooleanField(default=False)
    tools = models.ManyToManyField(Tool)

