from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Person


class CreatePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "last_name",
            "first_name"
        )

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "last_name",
            "first_name",
            "email"
        )