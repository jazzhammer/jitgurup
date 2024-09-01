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

@api_view(["POST", "GET", "DELETE", "PUT"])
def preferences(request: HttpRequest, *args, **kwargs):
    if request.method == 'PUT':
        id: str = request.data.get("id")
        if id:
            found = UserPreference.objects.get(pk=int(id), deleted=False)
            if found:
                name: str = request.data.get('name')
                if name:
                    if len(name.strip()) > 0:
                        found.name = name.strip()
                    else:
                        return JsonResponse({"error": f"require non blank name to update name, found {name=}"}, status=404, safe=False)
                value: str = request.data.get('value')
                if value:
                    if len(value.strip()) > 0:
                        found.value = value.strip()
                    else:
                        return JsonResponse({"error": f"require non blank value to update value, found {value=}"}, status=404, safe=False)
                user_id: str = request.data.get('user_id')
                if user_id:
                    if len(user_id.strip()) > 0:
                        try:
                            user_id: int = int(user_id)
                            found.user_id = user_id
                        except Exception as e:
                            return JsonResponse({"error": f"require valid user_id to update user_id, found {user_id=}"}, status=404, safe=False)
                    else:
                        return JsonResponse({"error": f"require non blank user_id to update user_id, found {user_id=}"}, status=404, safe=False)

                found.save()
                return JsonResponse({
                    "message": "success",
                    "updated": model_to_dict(found)
                })
            else:
                return JsonResponse({"error": f"none found to update for {id=}"}, status=404, safe=False)
        else:
            return JsonResponse({"error": f"require id, to update {id=}"}, status=400, safe=False)

    if request.method == 'DELETE':
        id: str = request.GET.get("id")
        if id:
            found = UserPreference.objects.get(pk=int(id), deleted=False)
            if found:
                found.deleted = True
                found.save()
                return JsonResponse({
                    "message": "success",
                    "deleted": model_to_dict(found)
                })
            else:
                return JsonResponse({"error": f"none found to delete for {id=}"}, status=404, safe=False)
        else:
            return JsonResponse({"error": f"require id, to delete {id=}"}, status=400, safe=False)

    if request.method == 'POST':
        user_id: str = request.data.get('user_id')
        name: str = request.data.get('name')
        value: str = request.data.get('value')
        if not user_id or len(user_id.strip()) == 0:
            return JsonResponse({"error": f"require user_id, found {user_id=}"}, status=400, safe=False)
        if not name or len(name.strip()) == 0:
            return JsonResponse({"error": f"require name, found {name=}"}, status=400, safe=False)
        if not value or len(value.strip()) == 0:
            return JsonResponse({"error": f"require value, found {value=}"}, status=400, safe=False)

        alreadys: QuerySet = UserPreference.objects.filter(user_id=int(user_id), name=name.strip().lower())
        if alreadys is None or alreadys.count() == 0:
            created = UserPreference.objects.create(user_id=int(user_id), name=name.strip().lower(), value=value.strip().lower())
            return JsonResponse({
                "message": "created UserPreference",
                "created": model_to_dict(created)
            }, status=201, safe=False)
        else:
            already = alreadys.first()
            already.value = value
            already.deleted = False
            already.save()
            return JsonResponse({
                "message": "updated UserPreference",
                "updated": model_to_dict(already)
            }, status=200, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        name = request.GET.get('name')
        if id:
            try:
                id = int(id)
                found = UserPreference.objects.get(pk=id, deleted=False)
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"error retrieving user_preference for {id=}"})
        filtered = False
        founds = UserPreference.objects.all()
        if user_id:
            try:
                user_id = int(user_id)
                founds = founds.filter(user_id=user_id)
                filtered = True
            except Exception as e:
                return JsonResponse({"message": f"error {e=} retrieving user_preference for {user_id=}"})
        if name and len(name.strip()) > 0:
            filtered = True
            founds = founds.filter(name__contains=name)
        if filtered:
            return JsonResponse({"message": "success", "data": [model_to_dict(instance) for instance in founds]}, status=200, safe=False)
        else:
            return JsonResponse({
                "message": f"require filter: id | name to retrieve user_preferences, found {id=}, {name=}",
                "data": []
            }, status=200, safe=False)
