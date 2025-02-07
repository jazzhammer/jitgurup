from django.contrib.auth.models import User
from django.db import models

from api.models.org import Org


class UserOrg(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    org = models.ForeignKey(Org, default=None, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'user_id', 'org_id'], name='user_org_idx')
        ]

    def __str__(self):
        return f"user[{self.user_id}]-org[{self.org_id}]"

    @staticmethod
    def assignUserDefault(user, org_name, org_description):
        found_org = Org.objects.filter(name=org_name).first()
        if found_org == None:
            created = UserOrg.objects.create(name=org_name)
            if created is not None:
                print(f"created org: {created.name}")
                created.description = org_description
                created.save()
                found_org = created
            else:
                print(f"unable to create org '{org_name}' for default assignment to user {user}")
        userOrgs = UserOrg.objects.filter(org_id=found_org["id"], user_id=user.id).first()
        if userOrgs is None:
            UserOrg.objects.create(user_id=user.id, org_id=found_org["id"])

    @staticmethod
    def assignUserDefaults(user):
        UserOrg.assignUserDefault(user, 'jitguru:community', "demonstrates distributed instruction and learning without a facility")
        UserOrg.assignUserDefault(user, 'jitguru:facility', "demonstrates distributed instruction and learning centered in one physical faciliity")
        UserOrg.assignUserDefault(user, 'jitguru:multifacility', "demonstrates distributed instruction and learning centered more than one physical faciliity")
