from django.forms import model_to_dict
from rest_framework.decorators import api_view

from api.models import UserOrg, Org
from django.http import JsonResponse

@api_view(["GET"])
def user_orgs(request, *args, **kwargs):
    user_id = int(request.query_params['user_id'])
    founds = UserOrg.objects.filter(user_id=user_id)
    userOrgDicts = [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
    orgDicts = []
    for userOrgDict in userOrgDicts:
        org = Org.objects.get(id=userOrgDict["org_id"])
        orgDict = model_to_dict(org, fields=[field.name for field in org._meta.fields])
        orgDicts.append(orgDict)
    return JsonResponse({
        "assigned": orgDicts
    })
