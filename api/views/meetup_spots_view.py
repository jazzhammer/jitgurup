from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models.facility import Facility
from api.models.meetup_spot import MeetupSpot
from api.models.spot_type import SpotType

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

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def meetup_spots(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = MeetupSpot.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"meetup_spot not found for delete {id=}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)



    if request.method == 'PUT':
        id: int = request.data.get('id')
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        facility_id: int = request.data.get('facility_id')
        spot_type_id: int = request.data.get('spot_type_id')
        try:
            found = MeetupSpot.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"meetup_spot not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = MeetupSpot.objects.all()
        dupes.exclude(id=id)
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name=name)
        if facility_id:
            facility_id = int(facility_id)
            try:
                facility = Facility.objects.get(pk=facility_id)
            except:
                return JsonResponse({
                    "error": f"require valid facility_id to update meetup_spot, found {facility_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(facility_id=facility_id)

        if spot_type_id:
            spot_type_id = int(spot_type_id)
            try:
                spot_type = SpotType.objects.get(pk=spot_type_id)
            except:
                return JsonResponse({
                    "error": f"require valid spot_type_id to update meetup_spot, found {spot_type_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(spot_type_id=spot_type_id)

        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already meetup_spot {name=} for {facility_id=}, {spot_type_id=}",
            }, status=400, safe=False)

        if description:
            if len(description.strip()) <= 0:
                description = description.strip()
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)
        found.name = name
        found.description = description
        found.facility = facility
        found.spot_type = spot_type
        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        spot_type_id: int = request.data.get('spot_type_id')
        facility_id: int = request.data.get('facility_id')

        dupes: QuerySet = MeetupSpot.objects.all()
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"spot_type requires name, found {name=}",
            }, status=400, safe=False)

        if not spot_type_id:
            return JsonResponse({
                "error": f"require spot_type, found {spot_type_id=}",
            }, status=400, safe=False)
        else:
            spot_type_id = int(spot_type_id)
            dupes = dupes.filter(spot_type_id=spot_type_id)

        if not facility_id:
            return JsonResponse({
                "error": f"require facility, found {facility_id=}",
            }, status=400, safe=False)
        else:
            facility_id = int(facility_id)
            dupes = dupes.filter(facility_id=facility_id)

        if description:
            if len(description.strip()) <= 0:
                return JsonResponse({
                    "error": f"require valid description if provided, found {description=}",
                }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(model_to_dict(dupe), status=201, safe=False)

        created = MeetupSpot.objects.create(
            name=name,
            description=description.strip(),
            spot_type_id=spot_type_id,
            facility_id=facility_id
        )
        return JsonResponse(model_to_dict(created), status=201, safe=False)


    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = MeetupSpot.objects.get(pk=id)
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no meetup_spot found for {id=}'
                }, status=404, safe=False)
        name = request.query_params['name'] if 'name' in request.query_params else None
        facility_id = request.query_params['facility_id'] if 'facility_id' in request.query_params else None
        if name is not None:
            found = MeetupSpot.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
        if facility_id is not None:
                founds = MeetupSpot.objects.filter(facility_id=facility_id)
                if founds is not None:
                    return JsonResponse([model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds], status=200, safe=False)

        else:
            return JsonResponse({
                "message": "require name or facility_id for meetup_spot query"
            }, status=400)