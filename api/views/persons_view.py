from django.db.models import QuerySet, Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.person import Person
from api.serializers.user_serializers import CreatePersonSerializer


@api_view(["POST", "GET"])
def persons(request: HttpRequest):

    if request.method == 'POST':
        new_person = JSONParser().parse(request)
        serializer = CreatePersonSerializer(data=new_person)
        if serializer.is_valid():
            created = Person.objects.create(**serializer.validated_data)
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
        if filtered:
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)