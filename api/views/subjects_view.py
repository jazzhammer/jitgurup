import io

from django.forms import model_to_dict
from rest_framework.decorators import api_view

from api.models.subject import Subject
from django.http import JsonResponse, HttpRequest


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def subjects(request: HttpRequest, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if not id:
            return JsonResponse({
                "error": f"require id to delete subject, found {id=}"
            }, status=400, safe=False)
        else:
            found = Subject.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"subject not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200)

    if request.method == 'PUT':
        id = request.data.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to update subject, found {id=}"
            }, status=400, safe=False)
        else:
            found = Subject.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"subject not found for {id=}"
                }, status=404, safe=False)

            name: str = request.data.get("name")
            if name:
                if len(name.strip()) > 0:
                    found.name = name.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank name to update subject, found {name=}"
                    }, status=400, safe=False)
            return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        if name:
            if len(name.strip()) > 0:
                already = Subject.objects.filter(name__iexact=name).first()
                if already is None:
                    created = Subject.objects.create(name=name.strip())
                    return JsonResponse(model_to_dict(created, fields=[field.name for field in created._meta.fields]), status=201, safe=False)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=200)
            else:
                return JsonResponse({
                    "error": f"require non blank name for new subject, found {name=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400, safe=False)

    elif request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = Subject.objects.get(pk=id)
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no subject found for {id=}'
                }, status=404, safe=False)

        name = request.GET.get('name')
        if name:
            founds = Subject.objects.filter(name__icontains=name, deleted=False)
            if founds is not None:
                return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
            else:
                return JsonResponse({
                    "message": f"no subject of name {name} found"
                }, status=404)
        else:
            founds = Subject.objects.all()[:10]
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)


