from rest_framework.serializers import ModelSerializer

from api.models.person_in_meetup import PersonInMeetup


class PersonInMeetupSerializer(ModelSerializer):
    class Meta:
        model = PersonInMeetup
        fields = (
            'person_id',
            'meetup_id',
            'meetup_role_id',
        )