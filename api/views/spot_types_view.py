import io

import psycopg2
from django.db.models import QuerySet
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.spot_type import SpotType
from django.http import JsonResponse, HttpRequest

from api.serializers.spot_type_serializer import SpotTypeSerializer
from jitgurup.settings import DATABASES

def reset_tests(request: HttpRequest):
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


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def spot_types(request):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = SpotType.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"spot_type not found for update {id=}",
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
            found = SpotType.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"spot_Type not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = SpotType.objects.all()
        dupes.exclude(id=id)
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name=name)
        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already a spot_Type {name=}",
            }, status=400, safe=False)
        if description:
            description = description.strip()
            if len(description) <= 0:
                return JsonResponse({
                    "error": f"require non blank description if provided",
                }, status=400, safe=False)

        found.name = name
        found.description = description
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        description: str = request.data.get('description')
        dupes: QuerySet = SpotType.objects.all()
        if name:
            if len(name.strip()) <= 0:
                return JsonResponse({
                    "error": f"require name",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(name__iexact=name.strip())
        else:
            return JsonResponse({
                "error": f"spot_type requires name, found {name=}",
            }, status=400, safe=False)

        if description:
            if len(description.strip()) <= 0:
                return JsonResponse({
                    "error": f"require valid description if provided, found {description=}",
                }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(model_to_dict(dupe), status=201, safe=False)
        created = SpotType.objects.create(name=name, description=description)
        return JsonResponse(model_to_dict(created), status=201, safe=False)



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
        return JsonResponse(spot_typeDicts, status=200, safe=False)

    elif request.method == "POST":
        body = request.body
        newSpotType = JSONParser.parse(io.BytesIO(body))
        already = SpotType.objects.filter(user_id=newSpotType['user_id'], spot_type_id=newSpotType['spot_type_id']).first()
        if already is None:
            serializer = SpotTypeSerializer(data=newSpotType)
            if serializer.is_valid():
                SpotType.objects.create(**serializer.validated_data)
                return JsonResponse(serializer.validated_data, status=201)
            else:
                return JsonResponse({
                    "message": "failure. unable to create SpotType"
                }, status=400)
        else:
            return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=400)
