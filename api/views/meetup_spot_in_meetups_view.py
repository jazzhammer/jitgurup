from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import MeetupSpotInMeetup
from api.serializers.meetup_spot_in_meetup_serializer import MeetupSpotInMeetupSerializer


@api_view(["POST", "GET"])
def meetup_spot_in_meetups(request, meetup_spot_in_meetup_id, **kwargs):

    if request.method == 'POST':
        new_meetup_spot_in_meetup = JSONParser().parse(request)
        serializer = MeetupSpotInMeetupSerializer(data=new_meetup_spot_in_meetup)
        if serializer.is_valid():
            MeetupSpotInMeetup.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        if meetup_spot_in_meetup_id is not None:
            found = MeetupSpotInMeetup.objects.get(id=meetup_spot_in_meetup_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
