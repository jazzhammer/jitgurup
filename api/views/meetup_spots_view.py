from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.meetup_spot import MeetupSpot
from api.serializers.meetup_spot_serializer import MeetupSpotSerializer


@api_view(['GET'])
def meetup_spot(request, meetup_spot_id):
    found = MeetupSpot.objects.get(id=meetup_spot_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    MeetupSpot.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET'])
def meetup_spots(request, *args, **kwargs):
    if request.method == 'POST':
        newMeetupSpot = JSONParser().parse(request)
        already = MeetupSpot.objects.filter(name=newMeetupSpot['name']).first()
        if already is None:
            serializer = MeetupSpotSerializer(data=newMeetupSpot)
            if serializer.is_valid():
                created = MeetupSpot.objects.create(**serializer.validated_data)
                return JsonResponse({
                    "message": "success",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=201)
            else:
                return JsonResponse({
                    "message": "failure"
                }, status=400)
        else:
            return JsonResponse({
                "message": "previously created",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=200)

    if request.method == 'GET':
        name = request.query_params['name'] if 'name' in request.query_params else None
        facility_id = request.query_params['facility_id'] if 'facility_id' in request.query_params else None
        if name is not None:
            found = MeetupSpot.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse({
                    "message": "success",
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200)
        if facility_id is not None:
                founds = MeetupSpot.objects.filter(facility_id=facility_id)
                if founds is not None:
                    return JsonResponse({
                        "message": "success",
                        "matched": [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
                    }, status=200)

        else:
            return JsonResponse({
                "message": "require name or facility_id for meetup_spot query"
            }, status=400)