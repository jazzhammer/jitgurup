from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.template_role import TemplateRole
from api.models.crew_template import CrewTemplate

@api_view(['GET'])
def template_role(request, template_role_id):
    found = TemplateRole.objects.get(id=template_role_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    TemplateRole.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def template_roles(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = TemplateRole.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"template_role not found for update {id=}",
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
        max_count: int = request.data.get('max_count')
        description: str = request.data.get('description')
        crew_template_id: int = request.data.get('crew_template_id')
        try:
            found = TemplateRole.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"template_role not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = TemplateRole.objects.all().exclude(id=id)
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name=name)
        if crew_template_id:
            try:
                crew_template = CrewTemplate.objects.get(pk=crew_template_id)
            except:
                return JsonResponse({
                    "error": f"require valid crew_template_id to update crew_template_id, found {crew_template_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(crew_template_id=crew_template_id)
        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already template_role {name=} for {crew_template_id=}",
            }, status=400, safe=False)
        if description:
            if len(description.strip()) <= 0:
                description = description.strip()
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)
        if max_count is not None:
            found.max_count = max_count
        found.name = name
        found.description = description
        found.crew_template = crew_template
        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        max_count: int = request.data.get('max_count')
        crew_template_id: str = request.data.get('crew_template_id')
        dupes: QuerySet = TemplateRole.objects.all()
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"template_role requires name, found {name=}",
            }, status=400, safe=False)

        if crew_template_id:
            try:
                crew_template = CrewTemplate.objects.get(pk=crew_template_id)
            except:
                return JsonResponse({
                    "error": f"require valid crew_template_id to update crew_template_id, found {crew_template_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(crew_template_id=crew_template_id)
        else:
            return JsonResponse({
                "error": f"template_role requires name, found {name=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(model_to_dict(dupe), status=201, safe=False)
        created = TemplateRole.objects.create(
            name=name,
            crew_template=crew_template,
            description=description
        )
        if max_count is not None:
            created.max_count = max_count
            created.save()
        return JsonResponse(model_to_dict(created), status=201, safe=False)

    if request.method == 'GET':
        name = request.GET.get('name')
        crew_template_id = request.GET.get('crew_template_id')
        if name:
            found = TemplateRole.objects.filter(name=name).first()
            if found:
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            else:
                return JsonResponse([], status=200, safe=False)
        if crew_template_id:
                founds = TemplateRole.objects.filter(crew_template_id=crew_template_id)
                if founds:
                    return JsonResponse([model_to_dict(instance) for instance in founds], status=200)
                else:
                    return JsonResponse([], status=400, safe=False)

        else:
            return JsonResponse({
                "message": "require name or crew_template_id for template_role query"
            }, status=400, safe=False)