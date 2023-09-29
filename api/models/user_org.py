from django.db import models


class UserOrg(models.Model):
    user_id = models.IntegerField()
    org_id = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'org_id'], name='user_org_idx')
        ]
