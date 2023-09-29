from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.facility import Facility
from api.serializers.facility_serializer import FacilitySerializer

@api_view(['GET'])
def facility(request, facility_id):
    found = Facility.objects.get(id=facility_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    Facility.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET'])
def facilitys(request, *args, **kwargs):
    if request.method == 'POST':
        newFacility = JSONParser().parse(request)
        already = Facility.objects.filter(name=newFacility['name']).first()
        if already is None:
            serializer = FacilitySerializer(data=newFacility)
            if serializer.is_valid():
                created = Facility.objects.create(**serializer.validated_data)
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
        org_id = request.query_params['org_id'] if 'org_id' in request.query_params else None
        if name is not None:
            found = Facility.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse({
                    "message": "success",
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200)
        if org_id is not None:
                founds = Facility.objects.filter(org_id=org_id)
                if founds is not None:
                    return JsonResponse({
                        "message": "success",
                        "matched": [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
                    }, status=200)

        else:
            return JsonResponse({
                "message": "require name or org_id for facility query"
            }, status=400)