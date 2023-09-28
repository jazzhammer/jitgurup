from rest_framework.serializers import ModelSerializer
from api.models.user_preference import UserPreference


class UserPreferenceSerializer(ModelSerializer):
    class Meta:
        model = UserPreference
        fields = (
            'user_id',
            'name',
            'value'
        )