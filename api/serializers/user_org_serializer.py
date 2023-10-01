from rest_framework.serializers import ModelSerializer

from api.models.user_org import UserOrg


class UserOrgSerializer(ModelSerializer):
    class Meta:
        model = UserOrg
        fields = (
            'user_id',
            'org_id'
        )