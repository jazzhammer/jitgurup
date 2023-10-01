from rest_framework.serializers import ModelSerializer

from api.models import Meetup


class MeetupSerializer(ModelSerializer):
    class Meta:
        model = Meetup
        fields = (
            'start_at',
            'duration',
        )