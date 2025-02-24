from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.frequent_answer import FrequentAnswer
from api.models.frequent_question import FrequentQuestion

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def frequent_answers(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = FrequentAnswer.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"frequent_answer not found for update {id=}: {get_e}",
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
        frequent_question_id: int = request.data.get('frequent_question_id')
        try:
            found = FrequentAnswer.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"frequent_answer not found for update {id=}",
            }, status=404, safe=False)
        if frequent_question_id:
            try:
                frequent_question = FrequentQuestion.objects.get(pk=frequent_question_id)
            except:
                return JsonResponse({
                    "error": f"require valid frequent_question_id to update frequent_question_id, found {frequent_question_id=}",
                }, status=400, safe=False)
        if content:
            if len(content.strip()) <= 0:
                content = content.strip()
                return JsonResponse({
                    "error": f"require non blank content if provided",
                }, status=400, safe=False)
        found.content = content
        found.frequent_question = frequent_question
        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        content: str = request.data.get('content')
        frequent_question_id: str = request.data.get('frequent_question_id')
        if frequent_question_id:
            try:
                frequent_question = FrequentQuestion.objects.get(pk=frequent_question_id)
            except:
                return JsonResponse({
                    "error": f"require valid frequent_question_id to update frequent_question_id, found {frequent_question_id=}",
                }, status=400, safe=False)
        created = FrequentAnswer.objects.create(frequent_question=frequent_question, content=content)
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = FrequentAnswer.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no frequent_answer found for {id=}'
                }, status=404, safe=False)
        frequent_question_id = request.GET.get('frequent_question_id')
        founds = FrequentAnswer.objects.all();
        filtered = False
        if frequent_question_id:
            filtered = True
            founds = founds.filter(frequent_question_id=frequent_question_id)
        if not filtered:
            founds = FrequentAnswer.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(frequent_answer: dict):
    frequent_answer['frequent_question_id'] = frequent_answer.get('frequent_question')
    try:
        frequent_answer['frequent_question'] = model_to_dict(FrequentQuestion.objects.get(pk=frequent_answer['frequent_question_id']))
    except Exception as build_e:
        pass
    return frequent_answer