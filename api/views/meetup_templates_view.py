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

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def meetup_templates(request, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if id:
            try:
                found = MeetupTemplate.objects.get(pk=id)
            except:
                return JsonResponse({
                    "error": f"meetup_template not found for {id=}",
                }, status=404)
            found.deleted = True
            found.save()
            return JsonResponse({
                "message": "success",
                "deleted": model_to_dict(found)
            }, status=200)
        else:
            return JsonResponse({
                "error": f"meetup_template not found for {id=}",
            }, status=404)

    if request.method == 'PUT':
        id = request.data.get('id')
        if id:
            try:
                found = MeetupTemplate.objects.get(pk=id)
            except:
                return JsonResponse({
                    "error": f"meetup_template not found for {id=}",
                }, status=404)
            name: str = request.data.get('name')
            if name:
                try:
                    already = MeetupTemplate.objects.get(name__iexact=name.strip())
                except:
                    # ok. not a dupe if we change to this name
                    found.name = name.strip()
                    found.save()
                    return JsonResponse({
                        "message": "success",
                        "updated": model_to_dict(found)
                    }, status=201)
                if already:
                    # return the one we already have
                    already.deleted = False
                    already.save()
                    return JsonResponse({
                        "message": "success",
                        "updated": model_to_dict(already)
                    }, status=200)
            else:
                # noop
                return JsonResponse({
                    "message": "success",
                    "updated": model_to_dict(found)
                }, status=200)

    if request.method == 'POST':
        name = request.data.get('name')
        if name and len(name.strip()) > 0:
            try:
                already = MeetupTemplate.objects.get(name__iexact=name.strip())
            except:
                # good, not exist
                created = MeetupTemplate.objects.create(name=name)
                return JsonResponse({
                    "message": "success",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=201)
            else:
                already.deleted = False
                already.save()
                return JsonResponse({
                    "message": "previously created",
                    "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
                }, status=200)
        else:
            return JsonResponse({
                "error": f"require name for meetup_template, found {name=}",
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