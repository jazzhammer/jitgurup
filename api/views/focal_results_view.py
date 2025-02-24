from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.focal_result import FocalResult
from api.models.signup import Signup

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def focal_results(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = FocalResult.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"focal_result not found for update {id=}: {get_e}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(build(model_to_dict(found)), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        signup_id: int = request.data.get('signup_id')
        found = None
        if id:
            try:
                found = FocalResult.objects.get(pk=id)
            except Exception as id_e:
                return JsonResponse({
                    "error": f"require valid id to update focal_result, found {id=}",
                }, status=404, safe=False)
        else:
            return JsonResponse({
                "error": f"require valid id to update focal_result, found {id=}",
            }, status=404, safe=False)

        if signup_id:
            try:
                signup = Signup.objects.get(pk=signup_id)
                found.signup = signup
                found.save()
            except:
                return JsonResponse({
                    "error": f"require valid signup_id to update signup_id, found {signup_id=}",
                }, status=400, safe=False)

        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        signup_id: str = request.data.get('signup_id')
        if signup_id:
            try:
                signup = Signup.objects.get(pk=signup_id)
            except:
                return JsonResponse({
                    "error": f"require valid signup_id to update signup_id, found {signup_id=}",
                }, status=400, safe=False)
        created = FocalResult.objects.create(signup=signup)
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = FocalResult.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no focal_result found for {id=}'
                }, status=404, safe=False)
        signup_id = request.GET.get('signup_id')
        founds = FocalResult.objects.all();
        filtered = False
        if signup_id:
            filtered = True
            founds = founds.filter(signup_id=signup_id)
        if not filtered:
            founds = FocalResult.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(focal_result: dict):
    focal_result['signup_id'] = focal_result.get('signup')
    try:
        focal_result['signup'] = model_to_dict(Signup.objects.get(pk=focal_result['signup_id']))
    except Exception as signup_e:
        pass
    return focal_result