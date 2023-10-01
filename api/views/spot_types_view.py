import io

import psycopg2
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.spot_type import SpotType
from django.http import JsonResponse

from api.serializers.spot_type_serializer import SpotTypeSerializer
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
        cursor.execute("truncate api_spot_type")
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
def spot_type(request, spot_type_id):
    found = SpotType.objects.filter(id=spot_type_id).first()
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "no resource found"
        }, status=404)


@api_view(['POST', 'GET'])
def spot_types(request, *args, **kwargs):
    if request.method == 'POST':
        newSpotType = JSONParser().parse(request)
        if 'name' in newSpotType:
            already = SpotType.objects.filter(name=newSpotType['name']).first()
            if already is None:
                created = SpotType.objects.create(name=newSpotType['name'], description=newSpotType['description'])
                return JsonResponse({
                    "message": "created SpotType",
                    "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                }, status=200)
            else:
                return JsonResponse({
                    "message": "created SpotType",
                    "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
                }, status=200)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400)
    elif request.method == 'GET':
        name = request.query_params['name']
        if name is not None:
            found = SpotType.objects.filter(name=name).first()
            if found is not None:
                return JsonResponse({
                    "matched": model_to_dict(found, fields=[field.name for field in found._meta.fields])
                }, status=200)
            else:
                return JsonResponse({
                    "message": f"no spot_type of name {name} found"
                }, status=404)
        else:
            return JsonResponse({
                "message": f"require name to search for an SpotType"
            }, status=400)


@api_view(["GET", "POST"])
def user_spot_types(request, *args, **kwargs):
    if request.method == 'GET':
        user_id = int(request.query_params['user_id'])
        founds = SpotType.objects.filter(user_id=user_id)
        userSpotTypeDicts = [model_to_dict(found, fields=[field.name for field in found._meta.fields]) for found in founds]
        spot_typeDicts = []
        for userSpotTypeDict in userSpotTypeDicts:
            spot_type = SpotType.objects.get(id=userSpotTypeDict["spot_type_id"])
            spot_typeDict = model_to_dict(spot_type, fields=[field.name for field in spot_type._meta.fields])
            spot_typeDicts.append(spot_typeDict)
        return JsonResponse({
            "assigned": spot_typeDicts
        })

    elif request.method == "POST":
        body = request.body
        newSpotType = JSONParser.parse(io.BytesIO(body))
        already = SpotType.objects.filter(user_id=newSpotType['user_id'], spot_type_id=newSpotType['spot_type_id']).first()
        if already is None:
            serializer = SpotTypeSerializer(data=newSpotType)
            if serializer.is_valid():
                SpotType.objects.create(**serializer.validated_data)
                return JsonResponse({
                    "message": "success",
                    "created": serializer.validated_data
                }, status=201)
            else:
                return JsonResponse({
                    "message": "failure. unable to create SpotType"
                }, status=400)
        else:
            return JsonResponse({
                "message": "failed to create. previously created SpotType",
                "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
            }, status=400)
