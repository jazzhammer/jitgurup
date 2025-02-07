from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.person_in_meetup import PersonInMeetup
from api.serializers.person_in_meetup_serializer import PersonInMeetupSerializer

@api_view(["POST", "GET"])
def person_in_meets(request, person_in_meet_id, **kwargs):

    if request.method == 'POST':
        new_person_in_meet = JSONParser().parse(request)
        serializer = PersonInMeetupSerializer(data=new_person_in_meet)
        if serializer.is_valid():
            PersonInMeetup.objects.create(**serializer.validated_data)
            return JsonResponse(serializer.validated_data, status=201, safe=False)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    if request.method == 'GET':
        if person_in_meet_id is not None:
            found = PersonInMeetup.objects.get(id=person_in_meet_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200, safe=False)
