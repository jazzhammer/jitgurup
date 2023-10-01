from rest_framework.serializers import ModelSerializer

from api.models import MeetupRole


class MeetupRoleSerializer(ModelSerializer):
    class Meta:
        model = MeetupRole
        fields = (
            'name'
        )