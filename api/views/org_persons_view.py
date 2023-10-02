from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import OrgPerson
from api.serializers.org_person_serializer import OrgPersonSerializer


@api_view(["POST", "GET"])
def org_persons(request, org_person_id, **kwargs):

    if request.method == 'POST':
        new_org_person = JSONParser().parse(request)
        serializer = OrgPersonSerializer(data=new_org_person)
        if serializer.is_valid():
            OrgPerson.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        if org_person_id is not None:
            found = OrgPerson.objects.get(id=org_person_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
