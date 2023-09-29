from rest_framework.serializers import ModelSerializer

from api.models.facility import Facility


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            'name',
            'description'
        )