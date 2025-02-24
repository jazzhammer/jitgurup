from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.focal_artifact_type import FocalArtifactType
from api.models.org import Org

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def focal_artifact_types(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = FocalArtifactType.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"focal_artifact_type not found for update {id=}: {get_e}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(build(model_to_dict(found)), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        try:
            found = FocalArtifactType.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"focal_artifact_type not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = FocalArtifactType.objects.all()
        dupes.exclude(id=id)
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name=name)
        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already focal_artifact_type {name=}",
            }, status=400, safe=False)
        if description:
            if len(description.strip()) <= 0:
                description = description.strip()
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)
        found.name = name
        found.description = description
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        dupes: QuerySet = FocalArtifactType.objects.all()
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"focal_artifact_type requires name, found {name=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(build(model_to_dict(dupe)), status=201, safe=False)
        created = FocalArtifactType.objects.create(name=name, org=org, description=description)
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = FocalArtifactType.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no focal_artifact_type found for {id=}'
                }, status=404, safe=False)
        name = request.GET.get('name')
        founds = FocalArtifactType.objects.all();
        filtered = False
        if name is not None:
            if len(name.strip()) > 0:
                filtered = True
                founds = FocalArtifactType.objects.filter(name__icontains=name)
        if not filtered:
            founds = FocalArtifactType.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(focal_artifact_type: FocalArtifactType):
    try:
        pass
    except Exception as e:
        pass
    return dict