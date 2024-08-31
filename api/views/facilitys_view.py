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
        if not already:
            serializer = FacilitySerializer(data=newFacility)
            if serializer.is_valid():
                name = newFacility.get('name')
                description = newFacility.get('description')
                org_id = newFacility.get('org_id')
                created = Facility.objects.create(name=name, description=description, org_id=org_id)
                return JsonResponse({
                    "message": "success",
                    "created": model_to_dict(created)
                }, status=201, safe=False)
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
        name = request.GET.get('name')
        org_id = request.GET.get('org_id')
        if name:
            found = Facility.objects.filter(name=name).first()
            if found:
                return JsonResponse({
                    "message": "success",
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200, safe=False)
            else:
                return JsonResponse({
                    "message": "success",
                    "matched": []
                }, status=200, safe=False)
        if org_id:
                founds = Facility.objects.filter(org_id=org_id)
                if founds:
                    return JsonResponse({
                        "message": "success",
                        "matched": [model_to_dict(instance) for instance in founds]
                    }, status=200)
                else:
                    return JsonResponse({
                        "message": "success",
                        "matched": []
                    }, status=400, safe=False)

        else:
            return JsonResponse({
                "message": "require name or org_id for facility query"
            }, status=400, safe=False)