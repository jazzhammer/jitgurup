import http
import io
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from api.models import Person
from api.serializers import CreatePersonSerializer, CreateUserSerializer
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate
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
        cursor.execute("truncate api_meetup")
        cursor.execute("truncate api_meetuprole")
        cursor.execute("truncate api_person")
        cursor.execute("truncate api_profession")
        cursor.execute("truncate api_showup")
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
def reset_tests_security(request, *args, **kwargs):
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
        cursor.execute("delete from auth_user where is_superuser = false")
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


@api_view(["POST"])
def users(request, *args, **kwargs):
    if request.method == 'POST':
        body = request.body
        creds = JSONParser().parse(io.BytesIO(body))
        # if only a username, check dupe for existing username
        if 'username' in creds:
            if len(creds) == 1:
                found = User.objects.filter(username=creds['username']).first()
                if found is None:
                    return JsonResponse({
                        "message": f"found no User matching username {creds['username']}"
                    })
                else:
                    serialized = model_to_dict(
                        found, fields=[field.name for field in found._meta.fields if field.name != 'password']
                    )
                    return JsonResponse({
                        "message": f"found one User matching username {creds['username']}",
                        "matched": serialized
                    }, status=200)
            elif len(creds) == 2:
                if 'password' in creds:
                    # authenticate

                    # hashed = make_password(creds['password'])
                    found = authenticate(username=creds['username'], password=creds['password'])
                    if found is None:
                        return JsonResponse({
                            "message": "no user found matching credentials provided"
                        })
                    else:
                        serialized = model_to_dict(
                            found,
                            fields=[field.name for field in found._meta.fields if field.name != 'password']
                        )
                        return JsonResponse({
                            "message": "user found matching credentials provided",
                            "authenticated": serialized
                        })
        # else proceed to create user row
        serializer = CreateUserSerializer(data=creds)
        if serializer.is_valid():

            user = User.objects.create_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            user.last_name = serializer.validated_data['last_name']
            user.first_name = serializer.validated_data['first_name']
            user.save()

            # create default Person for this user
            return JsonResponse({
                "message": "success",
                "created": serializer.validated_data
            }, status=201)
        else:
            return JsonResponse({
                "message": "failure: minimum object field requirements not met"
            }, status=400)

    return JsonResponse({
        "message": "failure"
    }, status=404)
