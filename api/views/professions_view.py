from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from api.models.profession import Role

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def professions(request: HttpRequest, *args, **kwargs):
    if request.method == 'PUT':
        id = request.data.get('id')
        if id:
            try:
                id = int(id)
                found = Role.objects.get(pk=id)
                name = request.data.get('name')
                if name:
                    if len(name.strip()) > 0:
                        found.name = name
                    else:
                        return JsonResponse({"detail": f"require non blank name if updating profession.name, found {name=}"},
                                            status=400,
                                            safe=False
                        )
                found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except:
                return JsonResponse({"detail": f"require valid id to update profession, found {id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require id to update profession"}, status=400, safe=False)
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if id:
            try:
                found = Role.objects.get(pk=id)
                found.deleted = True
                found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as e:
                return JsonResponse({"detail": "error", "error": e}, status=500, safe=False)
        else:
            return JsonResponse({"detail": f"require id to delete profession"}, status=400, safe=False)
    if request.method == 'POST':
        name = request.data.get('name')
        if name:
            if len(name.strip()) > 0:
                already = Role.objects.filter(name=name).first()
                if not already:
                    created = Role.objects.create(name=name)
                    return JsonResponse(model_to_dict(created, fields=[field.name for field in created._meta.fields]), status=201, safe=False)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=200, safe=False)
            else:
                return JsonResponse({"detail": f"require non blank name for profession, found {name=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require name for profession, found {name=}"}, status=400, safe=False)
    if request.method == 'GET':
        name = request.GET.get('name')
        id = request.GET.get('id')
        if id:
            try:
                id = int(id)
                found = Role.objects.get(pk=id, deleted=False)
                if found:
                    return JsonResponse(model_to_dict(found), status=200, safe=False)
                else:
                    return JsonResponse({"message": f"not found for {id=}"}, status=404, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"error retrieving profession for {id=}"}, status=400, safe=False)
        if name:
            if len(name.strip()) > 0:
                founds = Role.objects.filter(name__contains=name.strip(), deleted=False)
                if founds:
                    return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
                else:
                    return JsonResponse([], status=200, safe=False)
            else:
                return JsonResponse({"message": f"error retrieving profession for {name=}"}, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "require name or facility_id for profession query"
            }, status=400)