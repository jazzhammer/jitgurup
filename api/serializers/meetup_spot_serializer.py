from rest_framework.serializers import ModelSerializer

from api.models.meetup_spot import MeetupSpot


class MeetupSpotSerializer(ModelSerializer):
    class Meta:
        model = MeetupSpot
        fields = (
            'name',
            'description',
            'spot_type_id',
            'facility_id'
        )