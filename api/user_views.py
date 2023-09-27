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
from api.apps import AppConfig


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

def confirmDefaultUser():
    print(f"confirmDefaultUser...")
    from django.contrib.auth.models import User
    found = User.objects.filter(username="jitguruadmin").first()
    if found is None:
        created = User.objects.create_user("jitguruadmin", "admin@jitguru.com", "ilovethejitguru")
        if created is not None:
            print(f"created default user: {created.username}")
            created.is_superuser = True
            created.is_staff = True
            created.last_name = 'jitguru'
            created.first_name = 'admin'
            created.save()
            found = User.objects.filter(username="jitguruadmin").first()
            return found
    else:
        return model_to_dict(found, fields=[field.name for field in found._meta.fields])

@api_view(["POST"])
def seed_default_users(request, *args, **kwargs):
    confirmed = confirmDefaultUser()
    return Response({
        "message": "success",
        "seeded": [confirmed]
    }, status=200)

def confirmDefaultOrgs():
    print(f"confirmDefaultOrgs...")
    from .models import Org
    defaultOrgs = []
    found = Org.objects.filter(name='jitguru:community').first()
    if found == None:
        created = Org.objects.create(name='jitguru:community')
        if created is not None:
            print(f"created org: {created.name}")
            created.description = "demonstrates distributed instruction and learning without a facility"
            created.save()
            found = Org.objects.filter(name='jitguru:community').first()
    defaultOrgs.append(model_to_dict(found, fields=[field.name for field in found._meta.fields]))

    found = Org.objects.filter(name='jitguru:facility').first()
    if found == None:
        created = Org.objects.create(name='jitguru:facility')
        if created is not None:
            print(f"created org: {created.name}")
            created.description = "demonstrates distributed instruction and learning centered in one physical faciliity"
            created.save()
            found = Org.objects.filter(name='jitguru:facility').first()
    defaultOrgs.append(model_to_dict(found, fields=[field.name for field in found._meta.fields]))

    found = Org.objects.filter(name='jitguru:multifacility').first()
    if found == None:
        created = Org.objects.create(name='jitguru:multifacility')
        if created is not None:
            print(f"created org: {created.name}")
            created.description = "demonstrates distributed instruction and learning centered more than one physical faciliity"
            created.save()
            found = Org.objects.filter(name='jitguru:multifacility').first()
    defaultOrgs.append(model_to_dict(found, fields=[field.name for field in found._meta.fields]))
    return defaultOrgs

@api_view(["POST"])
def seed_default_orgs(request, *args, **kwargs):
    confirmedOrgs = confirmDefaultOrgs()
    return Response({
        "message": "success",
        "seeded": confirmedOrgs
    }, status=200)


def confirmUserOrgs():
    print(f"confirmUserOrgs()...")
    from .models import UserOrg
    from .models import Org
    from django.contrib.auth.models import User

    admin = User.objects.filter(username='jitguruadmin').first()
    userOrgs = []

    orgCommunity = Org.objects.filter(name='jitguru:community').first()
    orgCommunityDict = model_to_dict(orgCommunity, fields=[field.name for field in orgCommunity._meta.fields])
    userOrg = UserOrg.objects.filter(org_id=orgCommunityDict["id"], user_id=admin.id).first()
    if userOrg is None:
        UserOrg.objects.create(user_id=admin.id, org_id=orgCommunityDict["id"])
        userOrg = UserOrg.objects.filter(org_id=orgCommunityDict["id"], user_id=admin.id).first()
    userOrgs.append(userOrg)

    orgFacility = Org.objects.filter(name='jitguru:facility').first()
    orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
    userOrg = UserOrg.objects.filter(org_id=orgFacilityDict["id"], user_id=admin.id).first()
    if userOrg is None:
        UserOrg.objects.create(user_id=admin.id, org_id=orgFacilityDict["id"])
        userOrg = UserOrg.objects.filter(org_id=orgFacilityDict["id"], user_id=admin.id).first()
    userOrgs.append(userOrg)

    orgMultifacility = Org.objects.filter(name='jitguru:multifacility').first()
    orgMultifacilityDict = model_to_dict(orgMultifacility,
                                         fields=[field.name for field in orgMultifacility._meta.fields])
    userOrg = UserOrg.objects.filter(org_id=orgMultifacilityDict["id"], user_id=admin.id).first()
    if userOrg is None:
        UserOrg.objects.create(user_id=admin.id, org_id=orgMultifacilityDict["id"])
        userOrg = UserOrg.objects.filter(org_id=orgMultifacilityDict["id"], user_id=admin.id).first()
    userOrgs.append(userOrg)

    return [model_to_dict(userOrg, fields=[field.name for field in userOrg._meta.fields]) for userOrg in userOrgs]

@api_view(["POST"])
def seed_default_user_orgs(request, *args, **kwargs):
    confirmed = confirmUserOrgs()
    return JsonResponse({
        "message": "success",
        "seeded": confirmed
    }, status=200)
