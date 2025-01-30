from rest_framework.serializers import ModelSerializer

from api.models.meetup_role import MeetupRole


class MeetupRoleSerializer(ModelSerializer):
    class Meta:
        model = MeetupRole
        fields = (
            'name'
        )