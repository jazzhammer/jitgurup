import io

import psycopg2
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.user_org import UserOrg
from api.models.org import Org
from django.http import JsonResponse

from api.serializers.user_serializers import CreateUserOrgSerializer

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def orgs(request, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        found = None
        try:
            found = Org.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"not found for {id=}"
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
        description: str = request.data.get('description')
        try:
            found = Org.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"unable to update org not found for {id=}"
            }, status=404)
        if name:
            if len(name.strip()) > 0:
                name = name.strip()
                found.name = name
        if description:
            if len(description.strip()) > 0:
                description = description.strip()
                found.description = description
        found.save()
        return JsonResponse(model_to_dict(found), status=200)

    if request.method == 'POST':
        name: str = request.data.get('name')
        if name:
            if len(name.strip()) > 0:
                name = name.strip()
                try:
                    already = Org.objects.get(name__iexact=name)
                except:
                    try:
                        description = request.data.get('description')
                    except:
                        pass
                    if description is None:
                        description = 'this org requires a description'
                    created = Org.objects.create(name=name, description=description)

                    return JsonResponse(model_to_dict(created, fields=[field.name for field in created._meta.fields]), status=201)
                return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=200)
            else:
                return JsonResponse({
                    "message": f"unable to create for blank name, found {name=}"
                }, status=400)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400)

    elif request.method == 'GET':
        name = request.GET.get('name')
        description = request.GET.get('description')
        filtered = False
        founds = Org.objects.filter(deleted=False).order_by('name')
        if name:
            if len(name.strip()) > 0:
                filtered = True
                founds = founds.filter(name__icontains=name)
        if description:
            if len(description.strip()) > 0:
                filtered = True
                founds = founds.filter(description__icontains=description)
        if not filtered:
            founds = Org.objects.all().order_by('name')[:10]
        return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)

@api_view(["GET", "POST"])
def user_orgs(request, *args, **kwargs):
    if request.method == 'GET':
        user_id = int(request.query_params['user_id'])
        founds = UserOrg.objects.filter(user_id=user_id)
        userOrgDicts = [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
        orgDicts = []
        for userOrgDict in userOrgDicts:
            org = Org.objects.get(id=userOrgDict["org"])
            orgDict = model_to_dict(org, fields=[field.name for field in org._meta.fields])
            orgDicts.append(orgDict)
        return JsonResponse(orgDicts, status=200, safe=False)

    elif request.method == "POST":
        body = request.body
        newUserOrg = JSONParser.parse(io.BytesIO(body))
        already = UserOrg.objects.filter(user_id=newUserOrg['user_id'], org_id=newUserOrg['org_id']).first()
        if already is None:
            serializer = CreateUserOrgSerializer(data=newUserOrg)
            if serializer.is_valid():
                Org.objects.create(**serializer.validated_data)
                return JsonResponse(serializer.validated_data, status=201, safe=False)
            else:
                return JsonResponse({
                    "message": "failure. unable to create UserOrg"
                }, status=400)
        else:
            return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=400)
