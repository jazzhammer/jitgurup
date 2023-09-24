from rest_framework import serializers

from api.models import Person


class CreatePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "last_name",
            "first_name"
        )