from rest_framework.serializers import ModelSerializer

from api.models.user_meetup_spot import UserMeetupSpot


class UserMeetupSpotSerializer(ModelSerializer):
    class Meta:
        model = UserMeetupSpot
        fields = (
            'user_id',
            'meetup_spot_id'
        )