import io
import json

import psycopg2
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.user import UserOrg
from api.models.org import Org
from django.http import JsonResponse

from api.serializers.org_serializer import OrgSerializer
from api.serializers.user_serializers import CreateUserOrgSerializer
from jitgurup.settings import DATABASES

def reset_tests(request, *args, **kwargs):
    try:
        default_db = DATABASES["default"]
        connection = psycopg2.connect(
            database=default_db["NAME"],
            user=default_db["USER"],
            host=default_db["HOST"],
            port=default_db["PORT"],
            password=default_db["PASSWORD"]
        )
        cursor = connection.cursor()
        cursor.execute("truncate api_org")
        cursor.close()
        connection.commit()
        return JsonResponse({
            "message": "success"
        }, status=200)
    except KeyError as ke:
        return JsonResponse({
            "message": "failure",
            "error": f"error connecting to database, db connection details: {ke}"
        }, status=500)
    except psycopg2.Error as e:
        return JsonResponse({
            "message": "failure",
            "error": f"{e}"
        }, status=500)




@api_view(["GET"])
def org(request, org_id):
    found = Org.objects.filter(id=org_id).first()
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "no resource found"
        }, status=404)


@api_view(['POST', 'GET'])
def orgs(request, *args, **kwargs):
    if request.method == 'POST':
        newOrg = JSONParser().parse(request)
        if 'name' in newOrg:
            already = Org.objects.filter(name=newOrg['name']).first()
            if already is None:
                created = Org.objects.create(name=newOrg['name'], description=newOrg['description'])
                return JsonResponse({
                    "message": "created Org",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=200)
            else:
                return JsonResponse({
                    "message": "created Org",
                    "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
                }, status=200)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400)
    elif request.method == 'GET':
        name = request.query_params['name']
        if name is not None:
            found = Org.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse({
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200)
            else:
                return JsonResponse({
                    "message": f"no org of name {name} found"
                }, status=404)
        else:
            return JsonResponse({
                "message": f"require name to search for an Org"
            }, status=400)


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
        already = UserOrg.objects.filter(user_id=newUserOrg['user_id'], org_id=newUserOrg['org_id']).first()
        if already is None:
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
        else:
            return JsonResponse({
                "message": "failed to create. previously created UserOrg",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=400)
