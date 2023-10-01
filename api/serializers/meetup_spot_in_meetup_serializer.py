from rest_framework.serializers import ModelSerializer

from api.models.meetup_spot_in_meetup import MeetupSpotInMeetup


class MeetupSpotInMeetupSerializer(ModelSerializer):
    class Meta:
        model = MeetupSpotInMeetup
        fields = (
            'meetup_spot_id',
            'meetup_id',
        )