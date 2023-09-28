from rest_framework.serializers import ModelSerializer

from api.models.org import Org


class OrgSerializer(ModelSerializer):
    class Meta:
        model = Org
        fields = (
            'name',
            'description',
        )