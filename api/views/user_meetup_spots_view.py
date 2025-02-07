from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.user_meetup_spot import UserMeetupSpot
from api.serializers.user_meetup_spot_serializer import UserMeetupSpotSerializer


@api_view(['GET'])
def user_meetup_spot(request, user_meetup_spot_id):
    found = UserMeetupSpot.objects.get(id=user_meetup_spot_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    UserMeetupSpot.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET'])
def user_meetup_spots(request, *args, **kwargs):
    if request.method == 'POST':
        newUserMeetupSpot = JSONParser().parse(request)
        already = UserMeetupSpot.objects.filter(name=newUserMeetupSpot['name']).first()
        if already is None:
            serializer = UserMeetupSpotSerializer(data=newUserMeetupSpot)
            if serializer.is_valid():
                created = UserMeetupSpot.objects.create(**serializer.validated_data)
                return JsonResponse(
                    model_to_dict(created, fields=[field.name for field in created._meta.fields]),
                    status=201,
                    safe=False
                )
            else:
                return JsonResponse({"message": "failure"},
                                    status=400,
                                    safe=False
                )
        else:
            return JsonResponse(
                model_to_dict(
                    already,
                    fields=[field.name for field in already._meta.fields]
                ),
                status=200,
                safe=False
            )

    if request.method == 'GET':
        user_id = request.query_params['user_id'] if 'user_id' in request.query_params else None
        meetup_spot_id = request.query_params['meetup_spot_id'] if 'meetup_spot_id' in request.query_params else None
        if user_id is not None:
            # return all matching meetupSpots
            founds = UserMeetupSpot.objects.filter(user_id=user_id)
            if founds is not None:
                return JsonResponse(
                    [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds],
                    status=200,
                    safe=False
                )
        if meetup_spot_id is not None:
            founds = UserMeetupSpot.objects.filter(meetup_spot_id=meetup_spot_id)
            if founds is not None:
                return JsonResponse(
                    [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds],
                    status=200
                )

        else:
            return JsonResponse({
                "message": "require name or facility_id for user_meetup_spot query"
            }, status=400)