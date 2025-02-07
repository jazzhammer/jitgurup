from django.contrib.auth.models import User
from django.db import models
import uuid


class UserSession(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    session_id = models.CharField(max_length=38, null=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'session_id'], name='user_session_idx'),
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f"user[{self.user_id}]-session[{self.session_id}]"


    @classmethod
    def generate_uuid(cls):
        return uuid.uuid4()