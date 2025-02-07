from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from api.models.user_session import UserSession


@api_view(["GET", "POST", "PUT", "DELETE"])
def user_sessions(request: HttpRequest):
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
        return JsonResponse({"message": f"require id update UserSession. found {id=}"}, safe=False, status=404)
    session_id = request.data.get('session_id')
    if session_id:
        session_id = session_id.strip()
        if len(session_id) == 0 :
            return JsonResponse({"message": f"require session_id to update UserSession. found {session_id=}"}, safe=False, status=400)

    # check dupes
    dupes = UserSession.objects.filter(session_id=session_id).exclude(id=id)
    if len(dupes) > 0:
        return JsonResponse(
            {"message": f"require distinct session_id to update UserSession. found {session_id=}"},
            safe=False,
            status=400
        )
    else:
        found = UserSession.objects.get(pk=id)
        found.session_id = session_id
        found.save()
        return JsonResponse(model_to_dict(found), safe=False, status=200)

def delete(request: HttpRequest):
    id = request.GET.get('id')
    if id:
        try:
            found = UserSession.objects.get(pk=id)
            found.delete()
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        except Exception as get_e:
            return JsonResponse({"message": f"no UserSession for {id=}"}, status=404, safe=False)
    else:
        return JsonResponse({"message": f"require id to delete UserSession. found {id=}"}, status=400, safe=False)

def post(request: HttpRequest):
    session_id = request.data.get('session_id')
    if session_id:
        session_id = session_id.strip()

    # dupe ?
    founds = UserSession.objects.filter(session_id=session_id)
    if len(founds) > 0:
        return JsonResponse({"message": f"user_session {session_id=} already exists"}, status=400, safe=False)
    else:
        if session_id and len(session_id) > 0:
            created = UserSession.objects.create(session_id=session_id)
            return JsonResponse(model_to_dict(created), status=201, safe=False)
        return JsonResponse({"message": f"require session_id for UserSession, found {session_id=}, {description=}"}, safe=False, status=400)

def get(request: HttpRequest):
    id = request.GET.get('id')
    if id:
        if not isinstance(id, int):
            id = int(id)
    session_id = request.GET.get('session_id')

    if id:
        try:
            found = UserSession.objects.get(pk=id)
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        except Exception as get_e:
            return JsonResponse({"message": f"no UserSession for {id=}"}, status=404, safe=False)
    filtered = False
    founds = UserSession.objects.all()
    if session_id and len(session_id) > 0:
        filtered = True
        founds = founds.filter(session_id__iexact=session_id)

    if filtered:
        return JsonResponse([model_to_dict(found) for found in founds], safe=False, status=200)
    else:
        founds = founds.order_by('session_id')[:5]
        return JsonResponse([model_to_dict(found) for found in founds], safe=False, status=200)
