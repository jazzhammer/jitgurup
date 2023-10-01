from rest_framework.serializers import ModelSerializer

from api.models import Person


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'last_name',
            'first_name',
        )