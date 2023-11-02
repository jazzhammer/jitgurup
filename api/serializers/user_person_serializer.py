from rest_framework.serializers import ModelSerializer

from api.models.user_person import UserPerson


class UserPersonSerializer(ModelSerializer):
    class Meta:
        model = UserPerson
        fields = (
            'user_id',
            'person_id'
        )