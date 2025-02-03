from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.learning_modality import LearningModality



@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def learning_modalitys(request):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = LearningModality.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"learning_modality not found for update {id=}",
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
        try:
            found = LearningModality.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"learning_modality not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = LearningModality.objects.all()
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
                "error": f"already learning_modality {name=} for {name=}",
            }, status=400, safe=False)
        found.name = name
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        if name:
            name = name.strip()
        if not name:
            return JsonResponse({
                "error": f"require name",
            }, status=400, safe=False)

        created = LearningModality.objects.create(name=name)
        return JsonResponse(model_to_dict(created), status=201, safe=False)

    if request.method == 'GET':
        name = request.GET.get('name')
        id = request.GET.get('id')
        if name:
            found = LearningModality.objects.filter(name=name).first()
            if found:
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            else:
                return JsonResponse([], status=200, safe=False)
        if id:
            found = LearningModality.objects.get(pk=id)
            if found:
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            else:
                return JsonResponse([], status=400, safe=False)

        else:
            return JsonResponse({
                "message": "require name or learning_modality_template_id for learning_modality query"
            }, status=400, safe=False)