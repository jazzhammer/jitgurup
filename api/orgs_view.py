import io

from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import UserOrg, Org
from django.http import JsonResponse

from api.serializers import CreateOrgSerializer, CreateUserOrgSerializer


@api_view(["GET", "POST"])
def user_orgs(request, *args, **kwargs):
    if request.method == 'GET':
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

    elif request.method == "POST":
        body = request.body
        newUserOrg = JSONParser.parse(io.BytesIO(body))
        serializer = CreateUserOrgSerializer(data=newUserOrg)
        if serializer.is_valid():
            Org.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure. unable to create UserOrg"
            }, status=400)
