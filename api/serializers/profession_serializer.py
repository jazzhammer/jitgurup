from rest_framework.serializers import ModelSerializer

from api.models import Profession


class ProfessionSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = (
            'name',
        )