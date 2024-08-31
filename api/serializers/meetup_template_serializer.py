import rest_framework.serializers

from api.models.meetup_template import MeetupTemplate


class MeetupTemplateSerializer(rest_framework.serializers.ModelSerializer):

    class Meta:
        model = MeetupTemplate

        fields = [
            'name'
        ]
