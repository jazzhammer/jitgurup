import io

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.user_preference import UserPreference
from api.serializers.user_preference_serializer import UserPreferenceSerializer
from django.contrib.auth.models import User

@api_view(["POST", "GET"])
def preferences(request, *args, **kwargs):
    if request.method == 'POST':
        # body = request.body
        newUserPreference = JSONParser().parse(request)
        # if already, update
        already = UserPreference.objects.filter(user_id=newUserPreference["user_id"], name=newUserPreference["name"]).first()
        if already is None:
            serializer = UserPreferenceSerializer(data=newUserPreference)
            if serializer.is_valid():
                created = UserPreference.objects.create(**serializer.validated_data)
                return JsonResponse({
                    "message": "created UserPreference",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=201)
            else:
                return JsonResponse({
                    "message": "unable to create UserPreference for invalid fields"
                }, status=201)
        else:
            already.value = newUserPreference['value']
            already.save()
            return JsonResponse({
                "message": "updated existing UserPreference",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=201)

    if request.method == 'GET':
        pass

@api_view(['POST'])
def reset_tests(request, *args, **kwargs):
    User.objects.filter().exclude(username='jitguruadmin').delete()
    UserPreference.objects.all().delete()
    return JsonResponse({
        "message": "success",
        "deleted": "all"
    }, status=200)