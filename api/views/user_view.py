import http
import io
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User

from api.models.org import Org
from api.models.person import Person
from api.models.user_org import UserOrg
from api.serializers.user_serializers import CreatePersonSerializer, CreateUserSerializer
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth import authenticate
import psycopg2
from jitgurup.settings import DATABASES


@api_view(['GET'])
def user_user_groups(request):
    user = User.objects.get(id=int(request.query_params['user_id']))
    if user is None:
        return JsonResponse({
            "message": "failure"
        }, status=404)
    groups = user.groups.all()
    result = []
    for group in groups:
        result.append(model_to_dict(group, [field.name for field in group._meta.fields]))
    return JsonResponse({
        'user_groups': result
    }, status=200)

@api_view(['GET'])
def user(request, user_id):
    found = User.objects.get(id=user_id)
    if found is None:
        return JsonResponse({
            "message": "failure"
        }, status=404)
    else:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)

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


@api_view(["POST", "GET"])
def users(request, *args, **kwargs):
    if request.method == 'GET':
        id: str = request.GET.get('id')
        if id:
            try:
               found = User.objects.get(pk=int(id))
               user_dict = model_to_dict(
                   found,
                   fields=[field.name for field in found._meta.get_fields() if field.name != 'password']
               )
               return JsonResponse({"message": "success", "data": user_dict})
            except Exception as e:
                return JsonResponse({"error": f"error retrieving user for {id=}"}, status=400, safe=False)
        # last_login
        # is_staff
        # is_active
        # date_joined
        # is_superuser
        username: str = request.GET.get('username')
        first_name: str = request.GET.get('first_name')
        last_name: str = request.GET.get('last_name')
        email: str = request.GET.get('email')
        filtered = False
        founds = User.objects.all()
        if username:
            try:
                username = username.strip()
                founds = founds.filter(username=username)
                filtered = True
            except Exception as e:
                return JsonResponse({"error": f"error retrieving user for {username=}"}, status=400, safe=False)
        if first_name:
            try:
                first_name = first_name.strip()
                founds = founds.filter(first_name=first_name)
                filtered = True
            except Exception as e:
                return JsonResponse({"error": f"error retrieving user for {first_name=}"}, status=400, safe=False)
        if last_name:
            try:
                last_name = last_name.strip()
                founds = founds.filter(last_name=last_name)
                filtered = True
            except Exception as e:
                return JsonResponse({"error": f"error retrieving user for {last_name=}"}, status=400, safe=False)
        if email:
            try:
                email = email.strip()
                founds = founds.filter(email=email)
                filtered = True
            except Exception as e:
                return JsonResponse({"error": f"error retrieving user for {last_name=}"}, status=400, safe=False)
        if filtered:
            return JsonResponse({"message": "success", "data": [model_to_dict(instance) for instance in founds]}, status=200, safe=False)
        else:
            return JsonResponse(    {   "message": "require at least 1 filter among email|last_name|first_name|username",
                                        "data": [model_to_dict(instance) for instance in founds]
                                    },
                                    status=200, safe=False
                                )
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
        #                             __
        #  ___________   ____ _____ _/  |_  ____
        # _/ ___\_  __ \_/ __ \\__  \\   __\/ __ \
        # \  \___|  | \/\  ___/ / __ \|  | \  ___/
        # \___  >__|    \___  >____  /__|  \___  >
        #     \/            \/     \/          \/ if not dupe
        already = User.objects.filter(username=creds['username']).first()
        if already is None:
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
                person = Person.objects.create(last_name=user.last_name, first_name=user.first_name)
                person.save()
                # assign default Org(s) for this user
                UserOrg.assignUserDefaults(user)

                del serializer.validated_data['password']
                serializer.validated_data['id'] = user.id
                return JsonResponse({
                    "message": "success",
                    "created": serializer.validated_data
                }, status=201)
            else:
                return JsonResponse({
                    "message": "failure: minimum object field requirements not met"
                }, status=400)
        return JsonResponse({
            "message": "failure. user previously created for that username",
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
    from api.models.org import Org
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
    from api.models.user_org import UserOrg
    from api.models.org import Org
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
