from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.meetup_template import MeetupTemplate
# from api.serializers.meetup_template_serializer import MeetupTemplateSerializer


@api_view(['GET'])
def meetup_template(request, meetup_template_id):
    found = MeetupTemplate.objects.get(id=meetup_template_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST', 'GET'])
def meetup_templates(request, *args, **kwargs):
    if request.method == 'POST':
        newMeetupTemplate = JSONParser().parse(request)
        already = MeetupTemplate.objects.filter(name=newMeetupTemplate['name']).first()
        if already is None:
            # serializer = MeetupTemplateSerializer(data=newMeetupTemplate)
            # if serializer.is_valid():
                created = MeetupTemplate.objects.create({})
                return JsonResponse({
                    "message": "success",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=201)
            # else:
            #     return JsonResponse({
            #         "message": "failure"
            #     }, status=400)
        else:
            return JsonResponse({
                "message": "previously created",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=200)

    if request.method == 'GET':
        name = request.query_params['name'] if 'name' in request.query_params else None
        facility_id = request.query_params['facility_id'] if 'facility_id' in request.query_params else None
        if name is not None:
            found = MeetupTemplate.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse({
                    "message": "success",
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200)
        if facility_id is not None:
                founds = MeetupTemplate.objects.filter(facility_id=facility_id)
                if founds is not None:
                    return JsonResponse({
                        "message": "success",
                        "matched": [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
                    }, status=200)

        else:
            return JsonResponse({
                "message": "require name or facility_id for meetup_template query"
            }, status=400)