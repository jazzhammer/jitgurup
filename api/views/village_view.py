from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from api.models.village import Village


@api_view(["GET", "POST", "PUT", "DELETE"])
def villages(request: HttpRequest):
    if request.method == 'POST':
        return post(request)
    if request.method == 'GET':
        return get(request)
    if request.method == 'DELETE':
        return delete(request)
    if request.method == 'PUT':
        return put(request)

def put(request: HttpRequest):
    id = request.data.get('id')
    if not id:
        return JsonResponse({"message": f"require id update Village. found {id=}"}, safe=False, status=404)
    name = request.data.get('name')
    if name:
        name = name.strip()
    description = request.data.get('description')
    if description:
        description = description.strip()
    if len(name) == 0 or len(description) == 0:
            return JsonResponse({"message": f"require name and description to update Village. found {name=}, {description=}"}, safe=False, status=400)

    # check dupes
    dupes = Village.objects.filter(name=name, description=description).exclude(id=id)
    if len(dupes) > 0:
        return JsonResponse(
            {"message": f"require destinct name and/or description to update Village. found {name=}, {description=}"},
            safe=False,
            status=400
        )
    else:
        found = Village.objects.get(pk=id)
        found.name = name
        found.description = description
        found.save()
        return JsonResponse(model_to_dict(found), safe=False, status=200)

def delete(request: HttpRequest):
    id = request.GET.get('id')
    if id:
        try:
            found = Village.objects.get(pk=id)
            if request.GET.get('erase'):
                found.delete()
            else:
                found.deleted = True
                found.save()
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        except Exception as get_e:
            return JsonResponse({"message": f"no Village for {id=}"}, status=404, safe=False)
    else:
        return JsonResponse({"message": f"require id to delete Village. found {id=}"}, status=400, safe=False)

def post(request: HttpRequest):
    name = request.data.get('name')
    if name:
        name = name.strip()
    description = request.data.get('description')
    if description:
        description = description.strip()

    # dupe ?
    founds = Village.objects.filter(name=name)
    if len(founds) > 0:
        return JsonResponse({"message": f"village {name=} already exists"}, status=400, safe=False)
    else:
        if name and len(name) > 0:
            if description and len(description) > 0:
                created = Village.objects.create(name=name, description=description)
                return JsonResponse(model_to_dict(created), status=201, safe=False)
        return JsonResponse({"message": f"require name, description for Village, found {name=}, {description=}"}, safe=False, status=400)

def get(request: HttpRequest):
    id = request.GET.get('id')
    name = request.GET.get('name')
    description = request.GET.get('description')

    if id:
        try:
            found = Village.objects.get(pk=id)
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        except Exception as get_e:
            return JsonResponse({"message": f"no Village for {id=}"}, status=404, safe=False)
    filtered = False
    founds = Village.objects.all()
    if name and len(name) > 0:
        filtered = True
        founds = founds.filter(name__icontains=name)
    if description and len(description) > 0:
        filtered = True
        founds = founds.filter(description__icontains=description)

    if filtered:
        return JsonResponse([model_to_dict(found) for found in founds], safe=False, status=200)
    else:
        founds = founds.order_by('name')[:5]
        return JsonResponse([model_to_dict(found) for found in founds], safe=False, status=200)
