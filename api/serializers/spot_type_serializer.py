from rest_framework.serializers import ModelSerializer

from api.models.spot_type import SpotType


class SpotTypeSerializer(ModelSerializer):
    class Meta:
        model = SpotType
        fields = (
            'name',
            'description',
        )