from django.db.models import QuerySet, Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.person import Person
from api.serializers.user_serializers import CreatePersonSerializer


@api_view(["POST", "GET", "PUT", "DELETE"])
def persons(request: HttpRequest):
    if request.method == 'DELETE':
        id: str = request.data.get('id')
        if id and len(id.strip()) > 0:
            found = Person.objects.get(pk=id)
            found.deleted = True
            found.save()
            return JsonResponse({
                "message": f"success",
                "updated": model_to_dict(found)
            }, status=200, safe=False)

        else:
            return JsonResponse({
                "error": f"unable to update person for {id=}"
            }, status=400, safe=False)
    if request.method == 'PUT':
        last_name: str = request.data.get('last_name')
        first_name: str = request.data.get('first_name')
        deleted: str = request.data.get('deleted')
        user_id: str = request.data.get('user_id')
        id: str = request.data.get('id')
        if id and len(id.strip()) > 0:
            try:
                found = Person.objects.get(pk=id, deleted=False)
            except Exception as e:
                return JsonResponse({
                    "error": f"unable to update person for {id=} {e=}"
                }, status=400, safe=False)

            if found:
                if last_name and len(last_name.strip()) > 0:
                    found.last_name = last_name
                if first_name and len(first_name.strip()) > 0:
                    found.first_name = first_name
                if user_id and len(user_id.strip()) > 0:
                    found.user_id = user_id
                found.save()
                return JsonResponse({
                    "message": f"success",
                    "updated": model_to_dict(found)
                }, status=200, safe=False)
            else:
                return JsonResponse({
                    "error": f"unable to update person for {id=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "error": f"unable to update person for {id=}"
            }, status=400, safe=False)
    if request.method == 'POST':
        new_person = JSONParser().parse(request)
        serializer = CreatePersonSerializer(data=new_person)
        if serializer.is_valid():
            created = Person.objects.create(**serializer.validated_data)
            user_id = request.data.get('user_id')
            if user_id and len(user_id.strip()) > 0:
                created.user_id = user_id
                created.user.save()
            return JsonResponse({
                "message": "success",
                "created": model_to_dict(created)
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        first_name: str = request.GET.get('first_name')
        last_name: str = request.GET.get('last_name')
        name: str = request.GET.get('name')
        user_id: str = request.GET.get('user_id')
        founds: QuerySet = Person.objects.all().filter(deleted=False)
        filtered = False
        if first_name and len(first_name.strip()) > 0:
            filtered = True
            founds = founds.filter(first_name=first_name.lower())
        if last_name and len(last_name.strip()) > 0:
            filtered = True
            founds = founds.filter(last_name=last_name.lower())
        if name and len(name.strip()) > 0:
            filtered = True
            name = name.lower()
            founds = founds.filter(Q(last_name__contains=name)|Q(first_name__contains=name))
        if user_id and len(user_id.strip()) > 0:
            filtered = True
            user_id = user_id.lower()
            founds = founds.filter(user_id=user_id)
        if filtered:
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)