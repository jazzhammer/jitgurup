from rest_framework.serializers import ModelSerializer

from api.models import OrgPerson


class OrgPersonSerializer(ModelSerializer):
    class Meta:
        model = OrgPerson
        fields = (
            'org_id',
            'person_id',
        )