from django.contrib.auth.models import User
from django.db import models


from api.models.org import Org

STATUS_NEW = 'N'
STATUS_APPROVED = 'A'
STATUS_DENIED = 'D'
STATUS_CANCELLED = 'C'

class OrgJoin(models.Model):
    org = models.ForeignKey(Org, default=None, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now=True, editable=True)
    cancelled_at = models.DateTimeField(auto_now=False, null=True)
    approved_at = models.DateTimeField(auto_now=False, null=True)
    denied_at = models.DateTimeField(auto_now=False, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'org_id', 'user_id', 'status']),
            models.Index(fields=['status', 'user_id']),
            models.Index(fields=['user_id', 'status']),
        ]

    def __str__(self):
        return f"org_id[{self.org_id}]-user_id[{self.user_id}]"

