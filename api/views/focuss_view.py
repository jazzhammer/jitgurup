import io

from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.focus import Focus
from django.http import JsonResponse, HttpRequest


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def focuss(request: HttpRequest, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to delete focus, found {id=}"
            }, status=400, safe=False)
        else:
            found = Focus.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"focus not found for {id=}"
                }, status=404, safe=False)
            else:
                found.deleted = True
                found.save()
                return JsonResponse({
                    "message": "success",
                    "deleted": model_to_dict(found)
                }, status=200)

    if request.method == 'PUT':
        id = request.data.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to update focus, found {id=}"
            }, status=400, safe=False)
        else:
            found = Focus.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"focus not found for {id=}"
                }, status=404, safe=False)

            name: str = request.data.get("name")
            if name:
                if len(name.strip()) > 0:
                    found.name = name.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank name to update focus, found {name=}"
                    }, status=400, safe=False)
            return JsonResponse({
                "message": "success",
                "updated": model_to_dict(found)
            }, status=200)

    if request.method == 'POST':
        name: str = request.data.get('name')
        if name:
            if len(name.strip()) > 0:
                already = Focus.objects.filter(name__iexact=name).first()
                if already is None:
                    created = Focus.objects.create(name=name.strip())
                    return JsonResponse({
                        "message": "created Focus",
                        "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                    }, status=201)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse({
                        "message": "undeleted Focus",
                        "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
                    }, status=200)
            else:
                return JsonResponse({
                    "error": f"require non blank name for new focus, found {name=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400)

    elif request.method == 'GET':
        name = request.GET.get('name')
        if name:
            founds = Focus.objects.filter(name__icontains=name, deleted=False)
            if founds is not None:
                return JsonResponse({
                    "message": "success",
                    "matched": [model_to_dict(instance) for instance in founds]
                }, status=200)
            else:
                return JsonResponse({
                    "message": f"no focus of name {name} found"
                }, status=404)
        else:
            return JsonResponse({
                "message": f"require name to search for Focus"
            }, status=400)


