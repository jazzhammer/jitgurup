import os
from uuid import uuid4

from django.contrib.auth.models import User

from api.models.person import Person
from api.models.user_session import UserSession
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import psycopg2
from jitgurup.settings import DATABASES
from dotenv import load_dotenv
load_dotenv()

from django.contrib.auth import authenticate
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


@api_view(["POST", "GET", "DELETE"])
def users(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: str = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = User.objects.get(pk=id)
        except Exception as get_e:
            #   already erased
            return JsonResponse({'message': f'user not found for {id=}'}, status=404, safe=False)

        if found:
            if erase:
                found.delete()
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            else:
                found.deleted = True
                found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)
        else:
            return JsonResponse({'message': f"user not found for {id=}"}, status=200, safe=False)

    if request.method == 'GET':
        id: str = request.GET.get('id')
        group_name = request.GET.get('group_name')
        if group_name and group_name == 'common':
            try:
                common_username = os.getenv("DEFAULT_USERNAME")
                if common_username:
                    founds = User.objects.filter(username=common_username)
                    if len(founds) > 0:
                        found = founds[0]
                        session = UserSession.objects.create(user=found, session_id=uuid4())
                        found_dict = model_to_dict(found)
                        found_dict['session'] = model_to_dict(session)
                        return JsonResponse(found_dict, status=200, safe=False)
            except Exception as common_e:
                return JsonResponse({"message": f"error retrieving common users: {common_e}"}, status=500, safe=False)

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
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
        else:
            founds_dict = [model_to_dict(found, fields=[
                'id',
                'last_login',
                'is_superuser',
                'username',
                'first_name',
                'last_name',
                'email',
                'is_staff',
                'is_active',
                'date_joined'
            ]) for found in founds]

            return JsonResponse(
                founds_dict,
                status=200,
                safe=False
            )
    if request.method == 'POST':
        data = request.data
        if len(data) == 0:
            data = request.POST
        username = data.get("username")
        password = data.get("password")
        if password:
            if username:
                found = authenticate(username=username, password=password)
                if found:
                    user_session = UserSession.objects.create(user=found, session_id=UserSession.generate_uuid())
                    found['session_id'] = user_session.session_id
                    return JsonResponse(found, status=201, safe=False)
                else:
                    return JsonResponse({
                        "message": f"found no User matching creds provided"
                    }, status=404, safe=False)
        else:

            last_name = data.get("last_name")
            if last_name:
                last_name = last_name.strip()
            first_name = data.get("first_name")
            if first_name:
                first_name = first_name.strip()

            username = data.get("username")
            if username:
                founds = User.objects.filter(username=username)
                if founds and len(founds) > 0:
                    return JsonResponse({
                        "message": f"user exists with username provided",
                    }, status=400, safe=False)
                else:
                    # create user with default password
                    # else proceed to create user row
                    #                             __
                    #  ___________   ____ _____ _/  |_  ____
                    # _/ ___\_  __ \_/ __ \\__  \\   __\/ __ \
                    # \  \___|  | \/\  ___/ / __ \|  | \  ___/
                    # \___  >__|    \___  >____  /__|  \___  >
                    #     \/            \/     \/          \/ if not dupe
                    user = User.objects.create(last_name=last_name, first_name=first_name, username=username)
                    # create default Person for this user
                    person = Person.objects.create(last_name=user.last_name, first_name=user.first_name)
                    # assign default Org(s) for this user
                    # UserOrg.assignUserDefaults(user)

                    return JsonResponse(model_to_dict(user), status=201, safe=False)
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
