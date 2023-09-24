import http
import io
import json

from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

from api.models import Person
from api.serializers import CreatePersonSerializer
from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from django.http import JsonResponse

import psycopg2
from jitgurup.settings import DATABASES

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        # print(instance)
        data = serializer.data
        print(data)
        return Response(data)
    return Response({"error": "bad data"}, status=http.HTTPStatus.BAD_REQUEST)

    # return JsonResponse(data)

@api_view(["POST"])
def reset_tests(request, *args, **kwargs):
    print("reset_tests(request, *args, **kwargs):")
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
        cursor.execute("delete from api_meetup")
        cursor.execute("delete from api_meetuprole")
        cursor.execute("delete from api_person")
        cursor.execute("delete from api_profession")
        cursor.execute("delete from api_showup")
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

@api_view(["POST"])
def persons(request, *args, **kwargs):
    if request.method == 'POST':
        body = request.body
        new_person = JSONParser().parse(io.BytesIO(body))
        serializer = CreatePersonSerializer(data=new_person)
        if serializer.is_valid():
            Person.objects.create(**serializer.validated_data)
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)
    return JsonResponse({
        "message": "success"
    }, status=200)
