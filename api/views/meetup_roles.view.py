from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import MeetupRole
from api.serializers.meetup_role_serializer import MeetupRoleSerializer


@api_view(["POST", "GET"])
def meetup_roles(request, meetup_role_id, **kwargs):

    if request.method == 'POST':
        new_meetup_role = JSONParser().parse(request)
        serializer = MeetupRoleSerializer(data=new_meetup_role)
        if serializer.is_valid():
            MeetupRole.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        if meetup_role_id is not None:
            found = MeetupRole.objects.get(id=meetup_role_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
