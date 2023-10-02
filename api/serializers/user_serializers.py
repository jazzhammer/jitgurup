from django.contrib.auth.models import User
from rest_framework import serializers

from api.models.org import Org
from api.models.person import Person
from api.models.user_org import UserOrg


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

class CreateOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = (
            "name",
            "description"
        )

class CreateUserOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrg
        fields = (
            "user_id",
            "org_id"
        )


