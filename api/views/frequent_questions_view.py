from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.frequent_question import FrequentQuestion
from api.models.org import Org

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def frequent_questions(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = FrequentQuestion.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"frequent_question not found for update {id=}: {get_e}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(build(model_to_dict(found)), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        content: str = request.data.get('content')
        try:
            found = FrequentQuestion.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"frequent_question not found for update {id=}",
            }, status=404, safe=False)
        if content:
            if len(content.strip()) <= 0:
                content = content.strip()
                return JsonResponse({
                    "error": f"require non blank content if provided",
                }, status=400, safe=False)
        found.content = content
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        content: str = request.data.get('content')
        created = FrequentQuestion.objects.create(content=content)
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        content = request.GET.get("content")
        if id:
            try:
                found = FrequentQuestion.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no frequent_question found for {id=}'
                }, status=404, safe=False)
        founds = FrequentQuestion.objects.filter(content__icontains=content)
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(frequent_question: FrequentQuestion):
    # dict = model_to_dict(frequent_question)
    # org_id = dict.get('org')
    # dict['org_id'] = org_id
    try:
        pass
        # org = Org.objects.get(pk=org_id)
        # dict['org'] = model_to_dict(org)
    except Exception as build_e:
        pass
    return frequent_question