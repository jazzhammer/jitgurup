import io
import json

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.user_preference import UserPreference
from api.serializers.user_preference_serializer import UserPreferenceSerializer
from django.contrib.auth.models import User

@api_view(["POST", "GET"])
def preferences(request: HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        name = request.data.get('name')
        value = request.data.get('value')
        alreadys: QuerySet = UserPreference.objects.filter(user_id=user_id, name=name)
        if alreadys is None or alreadys.count() == 0:
            created = UserPreference.objects.create(user_id=user_id, name=name, value=value)
            return JsonResponse({
                "message": "created UserPreference",
                "created": model_to_dict(created)
            }, status=201, safe=False)
        else:
            already.value = value
            already.save()
            return JsonResponse({
                "message": "updated UserPreference",
                "updated": model_to_dict(already)
            }, status=200, safe=False)

    if request.method == 'GET':
        params = request.query_params
        if 'user_id' in params:
            founds = UserPreference.objects.filter(user_id=params['user_id'])
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
    UserPreference.objects.all().delete()
    return JsonResponse({
        "message": "success",
        "deleted": "all"
    }, status=200, safe=False)