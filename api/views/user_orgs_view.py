from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from api.models.org import Org
from api.models.user_org import UserOrg

@api_view(["POST", "GET", "DELETE"])
def user_orgs(request, *args, **kwargs):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                org_id = request.data.get('org_id')
                if org_id:
                    org = Org.objects.get(pk=org_id)
                    if org:
                        created = UserOrg.objects.create(user=user, org=org)
                        return JsonResponse(model_to_dict(created), status=201, safe=False)
                    else:
                        return JsonResponse({"message": f"require org for user_org, found {org_id=}"}, status=400, safe=False)
                else:
                    return JsonResponse({"message": f"require org for user_org, found {org_id=}"}, status=400,
                                        safe=False)
            else:
                return JsonResponse({"message": f"require user for user_org, found {user_id=}"}, status=400,
                                    safe=False)
        else:
            return JsonResponse({"message": f"require user for user_org, found {user_id=}"}, status=400,
                                safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        org_id = request.GET.get('org_id')

        if id:
            try:
                found = UserOrg.objects.get(pk=id)
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as get_e:
                return JsonResponse({"message": f"error getting user_org for {id=}"}, status=400, safe=False)
        founds = UserOrg.objects.all()
        filtered = False
        if user_id:
            filtered = True
            founds = founds.filter(user_id=user_id)
        if org_id:
            filtered = True
            founds = founds.filter(org_id=org_id)
        if filtered:
            return JsonResponse([model_to_dict(found) for found in founds], status=200, safe=False)
        else:
            return JsonResponse({
                "message": "require query-limiting param, eg. user_id",
            }, status=404)

    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if not id:
            return JsonResponse({
                "error": f"require id to delete user_org, found {id=}"
            }, status=400, safe=False)
        else:
            found = UserOrg.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"user_org not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)


@api_view(['POST'])
def reset_tests(request, *args, **kwargs):
    User.objects.filter().exclude(username='jitguruadmin').delete()
    UserOrg.objects.all().delete()
    return JsonResponse({
        "message": "success",
        "deleted": "all"
    }, status=200)