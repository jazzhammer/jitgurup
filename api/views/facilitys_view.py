from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.facility import Facility
from api.models.org import Org

@api_view(['GET'])
def facility(request, facility_id):
    found = Facility.objects.get(id=facility_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200, safe=False)
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

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def facilitys(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = Facility.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"facility not found for update {id=}: {get_e}",
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
        org_id: int = request.data.get('org_id')
        try:
            found = Facility.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"facility not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = Facility.objects.all()
        dupes.exclude(id=id)
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name=name)
        if org_id:
            try:
                org = Org.objects.get(pk=org_id)
            except:
                return JsonResponse({
                    "error": f"require valid org_id to update org_id, found {org_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(org_id=org_id)
        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already facility {name=} for {org_id=}",
            }, status=400, safe=False)
        if description:
            if len(description.strip()) <= 0:
                description = description.strip()
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)
        found.name = name
        found.description = description
        found.org = org
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        org_id: str = request.data.get('org_id')
        dupes: QuerySet = Facility.objects.all()
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"facility requires name, found {name=}",
            }, status=400, safe=False)

        if org_id:
            try:
                org = Org.objects.get(pk=org_id)
            except:
                return JsonResponse({
                    "error": f"require valid org_id to update org_id, found {org_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(org_id=org_id)
        else:
            return JsonResponse({
                "error": f"facility requires name, found {name=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(model_to_dict(dupe), status=201, safe=False)
        created = Facility.objects.create(name=name, org=org, description=description)
        return JsonResponse(model_to_dict(created), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = Facility.objects.get(pk=id)
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no facility found for {id=}'
                }, status=404, safe=False)
        name = request.GET.get('name')
        org_id = request.GET.get('org_id')
        founds = Facility.objects.all();
        filtered = False
        if name is not None:
            if len(name.strip()) > 0:
                filtered = True
                founds = Facility.objects.filter(name__icontains=name)
        if org_id:
            filtered = True
            founds = founds.filter(org_id=org_id)
        if not filtered:
            founds = Facility.objects.all()[:10]
        return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
