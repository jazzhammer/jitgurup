from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.crew import Crew
from api.models.crew_template import CrewTemplate


@api_view(['GET'])
def crew(request, crew_id):
    found = Crew.objects.get(id=crew_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    Crew.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def crews(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        try:
            found = Crew.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"crew not found for update {id=}",
            }, status=404, safe=False)
        found.deleted = True
        found.save()
        return JsonResponse({
            "message": "success",
            "deleted": model_to_dict(found)
        }, status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        name: str = request.data.get('name')
        crew_template_id: int = request.data.get('crew_template_id')
        try:
            found = Crew.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"crew not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = Crew.objects.all()
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
                "error": f"already crew {name=} for {crew_template_id=}",
            }, status=400, safe=False)
        found.name = name
        found.deleted = False
        return JsonResponse({
            "message": "success",
            "updated": model_to_dict(found)
        }, status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        if name:
            name = name.strip()
        if not name:
            return JsonResponse({
                "error": f"require name",
            }, status=400, safe=False)

        created = Crew.objects.create(name=name)
        return JsonResponse({
            "message": "success",
            "created": model_to_dict(created)
        }, status=201, safe=False)

    if request.method == 'GET':
        name = request.GET.get('name')
        crew_template_id = request.GET.get('crew_template_id')
        if name:
            found = Crew.objects.filter(name=name).first()
            if found:
                return JsonResponse({
                    "message": "success",
                    "matched": [model_to_dict(found)]
                }, status=200, safe=False)
            else:
                return JsonResponse({
                    "message": "success",
                    "matched": []
                }, status=200, safe=False)
        if crew_template_id:
                founds = Crew.objects.filter(crew_template_id=crew_template_id)
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
                "message": "require name or crew_template_id for crew query"
            }, status=400, safe=False)