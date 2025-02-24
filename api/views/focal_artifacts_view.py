from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.focal_artifact import FocalArtifact
from api.models.focal_artifact_type import FocalArtifactType
from api.models.focal_result import FocalResult


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def focal_artifacts(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = FocalArtifact.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"focal_artifact not found for update {id=}: {get_e}",
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
        focal_artifact_type_id: int = request.data.get('focal_artifact_type_id')
        focal_result_id: int = request.data.get('focal_result_id')
        try:
            found = FocalArtifact.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"focal_artifact not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = FocalArtifact.objects.all()
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
                "error": f"already focal_artifact {name=}",
            }, status=400, safe=False)
        if description:
            if len(description.strip()) <= 0:
                description = description.strip()
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)
        found.name = name
        found.description = description
        if focal_result_id:
            try:
                focal_result = FocalArtifactType.objects.get(pk=focal_result_id)
                found.focal_result = focal_result
            except Exception as type_e:
                return JsonResponse({
                    "error": f"require valid focal_result_id if provided, found {focal_result_id=}",
                }, status=400, safe=False)
        if focal_artifact_type_id:
            try:
                focal_artifact_type = FocalArtifactType.objects.get(pk=focal_artifact_type_id)
                found.focal_artifact_type = focal_artifact_type
            except Exception as type_e:
                return JsonResponse({
                    "error": f"require valid focal_artifact_type_id if provided, found {focal_artifact_type_id=}",
                }, status=400, safe=False)
        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        dupes: QuerySet = FocalArtifact.objects.all()

        focal_artifact_type_id: int = request.data.get('focal_artifact_type_id')
        focal_artifact_type = None

        focal_result_id: int = request.data.get('focal_result_id')
        focal_result = None

        if focal_artifact_type_id:
            try:
                focal_artifact_type = FocalArtifactType.objects.get(pk=focal_artifact_type_id)
            except Exception as type_e:
                return JsonResponse({
                    "error": f"require valid focal_artifact_type_id if provided, found {focal_artifact_type_id=}",
                }, status=400, safe=False)

        if focal_result_id:
            try:
                focal_result = FocalArtifactType.objects.get(pk=focal_result_id)
            except Exception as type_e:
                return JsonResponse({
                    "error": f"require valid focal_result_id if provided, found {focal_result_id=}",
                }, status=400, safe=False)

        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"focal_artifact requires name, found {name=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(build(model_to_dict(dupe)), status=201, safe=False)
        created = FocalArtifact.objects.create(
            name=name,
            focal_artifact_type=focal_artifact_type,
            focal_result=focal_result,
            description=description
        )
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = FocalArtifact.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no focal_artifact found for {id=}'
                }, status=404, safe=False)
        name = request.GET.get('name')
        founds = FocalArtifact.objects.all()
        filtered = False
        if name is not None:
            if len(name.strip()) > 0:
                filtered = True
                founds = FocalArtifact.objects.filter(name__icontains=name)
        focal_artifact_type_id = request.GET.get('focal_artifact_type_id')
        focal_result_id = request.GET.get('focal_result_id')
        if focal_artifact_type_id:
            try:
                filtered = True
                focal_artifact_type = FocalArtifactType.objects.get(pk=focal_artifact_type_id)
                filtered = filtered.filter(focal_artifact_type=focal_artifact_type)
            except Exception as filter_e:
                return JsonResponse({
                    'error:': f'no focal_artifact_type found for {focal_artifact_type_id=}'
                }, status=404, safe=False)

        if focal_result_id:
            try:
                filtered = True
                focal_result = FocalResult.objects.get(pk=focal_result_id)
                filtered = filtered.filter(focal_result=focal_result)
            except Exception as filter_e:
                return JsonResponse({
                    'error:': f'no focal_result found for {focal_result_id=}'
                }, status=404, safe=False)

        if not filtered:
            founds = FocalArtifact.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(focal_artifact: dict):
    try:
        focal_artifact['focal_result_id'] = focal_artifact.get('focal_result')
        focal_result = model_to_dict(FocalResult.objects.get(pk=focal_artifact['focal_result_id']))
        focal_artifact['focal_result'] = focal_result

        focal_artifact['focal_artifact_type_id'] = focal_artifact.get('focal_artifact_type')
        focal_artifact_type = model_to_dict(FocalArtifactType.objects.get(pk=focal_artifact['focal_artifact_type_id']))
        focal_artifact['focal_artifact_type'] = focal_artifact_type
    except Exception as build_e:
        print(f"error building focal artifact: {build_e}")
        pass
    return focal_artifact