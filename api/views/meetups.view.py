from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import Meetup
from api.serializers.meetup_serializer import MeetupSerializer


@api_view(["POST", "GET"])
def meetups(request, meetup_id, **kwargs):

    if request.method == 'POST':
        new_meetup = JSONParser().parse(request)
        serializer = MeetupSerializer(data=new_meetup)
        if serializer.is_valid():
            Meetup.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        if meetup_id is not None:
            found = Meetup.objects.get(id=meetup_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
