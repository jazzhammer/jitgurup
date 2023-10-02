import json

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import User

from api.models import UserPerson
from api.serializers.user_person_serializer import UserPersonSerializer


@api_view(["POST", "GET"])
def user_persons(request, *args, **kwargs):
    if request.method == 'POST':
        # body = request.body
        newUserPerson = JSONParser().parse(request)
        # if already, update
        already = UserPerson.objects.filter(user_id=newUserPerson["user_id"], name=newUserPerson["name"]).first()
        if already is None:
            serializer = UserPersonSerializer(data=newUserPerson)
            if serializer.is_valid():
                created = UserPerson.objects.create(**serializer.validated_data)
                return JsonResponse({
                    "message": "created UserPerson",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=201)
            else:
                return JsonResponse({
                    "message": "unable to create UserPerson for invalid fields"
                }, status=201)
        else:
            already.value = newUserPerson['value']
            already.save()
            return JsonResponse({
                "message": "updated existing UserPerson",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=201)

    if request.method == 'GET':
        params = request.query_params
        if 'user_id' in params:
            founds = UserPerson.objects.filter(user_id=params['user_id'])
            return JsonResponse(
                json.dumps(
                    [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
                ),
                status=200,
                safe=False
            )
        else:
            return JsonResponse({
                "message": "require query-limiting param, eg. user_id",
            }, status=404)

@api_view(['POST'])
def reset_tests(request, *args, **kwargs):
    User.objects.filter().exclude(username='jitguruadmin').delete()
    UserPerson.objects.all().delete()
    return JsonResponse({
        "message": "success",
        "deleted": "all"
    }, status=200)