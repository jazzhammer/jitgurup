from django.contrib.auth.models import User, Group
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models.org import Org
from api.models.org_join import OrgJoin, STATUS_NEW, STATUS_APPROVED, STATUS_CANCELLED, STATUS_DENIED
import smtplib, ssl
from dotenv import load_dotenv
load_dotenv()

import os
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_SMTP = os.getenv('ADMIN_SMTP')
ADMIN_SMTP_PASSWORD = os.getenv('ADMIN_SMTP_PASSWORD')
ADMIN_SMTP_PORT = os.getenv('ADMIN_SMTP_PORT')

@api_view(["POST", "GET"])
def org_joins(request):

    if request.method == 'PUT':
        id = request.data.get('id')
        found = None
        if id:
            try:
                found = OrgJoin.objects.get(pk=id)
            except Exception as e:
                return JsonResponse({"message": f"no org_join for {id=}"}, status=404, safe=False)


        status = request.data.get('status')
        org_id = request.data.get('org_id')
        if org_id:
            try:
                org = Org.objects.get(pk=org_id)
                found.org = org
                found.save()
            except Exception as e:
                return JsonResponse(
                    {"message": f"require valid org for org_join update. found {org_id=}"},
                    status=400,
                    safe=False
                )

        if status:
            try:
                if status in [STATUS_NEW, STATUS_APPROVED, STATUS_CANCELLED, STATUS_DENIED]:
                    found.status = status
                    found.save()
                else:
                    return JsonResponse(
                        {"message": f"require valid status for org_join update. found {status=}"},
                        status=400,
                        safe=False
                    )

            except Exception as e:
                return JsonResponse(
                    {"message": f"require valid status for org_join update. found {status=}"},
                    status=400,
                    safe=False
                )
        the_dict = model_to_dict(found)
        the_dict['created_at'] = f"{found.created_at}"
        return JsonResponse(build_dict(the_dict), status=200, safe=False)

    if request.method == 'POST':
        org_id = request.data.get('org_id')
        user_id = request.data.get('user_id')
        if org_id and user_id:
            try:
                org = Org.objects.get(pk=org_id)
                user = User.objects.get(pk=user_id)
                created = OrgJoin.objects.create(org=org, user=user)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(ADMIN_SMTP, ADMIN_SMTP_PORT, context=context) as server:
                    server.login(ADMIN_EMAIL, ADMIN_SMTP_PASSWORD)
                    sender_email = ADMIN_EMAIL
                    # notify admins
                    admins = Group.objects.get(name='admins')
                    if admins:
                        admin_users = User.objects.raw("""
                            select auth_user.* from 
                                auth_user, 
                                auth_user_groups, 
                                auth_group
                            where 
                                auth_group.user_id = auth_user.id
                            and auth_group.group_id = auth_group.id
                            and auth_group.name = 'admins'
                        """)
                        if len(admin_users) > 0:
                            sent_count = 0
                            for admin_user in admin_users:
                                if admin_user.email:
                                    try:
                                        receiver_email = admin_user.email
                                        message = f"new org join [{org.id=}]{org.name=}, [{user.id=}]{user.last_name=}, {user.first_name=}"
                                        server.sendmail(sender_email, receiver_email, message)
                                    except Exception as email_e:
                                        print(f"error email notification created org_join: {email_e}")
                        else:
                            print(f"no users found for group 'admins', for notifications")
                    else:
                        print(f"unable to notify for missing group: 'admins'")
                the_dict = model_to_dict(created)
                the_dict['created_at'] = f"{created.created_at}"
                return JsonResponse(build_dict(the_dict), status=201, safe=False)
            except Exception as e:
                return JsonResponse(
                    {"message": f"require org and user for org_join. found {org_id=}, {user_id=}"},
                    status=400,
                    safe=False
                )
        else:
            return JsonResponse({"message": f"require org and user for org_join. found {org_id=}, {user_id=}"}, status=400, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = OrgJoin.objects.get(pk=id)
                the_dict = model_to_dict(found)
                the_dict['created_at'] = f"{found.created_at}"
                return JsonResponse(build_dict(the_dict), status=200, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"no org_join for {id=}"}, status=404, safe=False)

        org_id = request.GET.get('org_id')
        user_id = request.GET.get('user_id')
        filtered = False
        founds = OrgJoin.objects.all().order_by('-created_at')
        if org_id:
            filtered = True
            founds = founds.filter(org_id=org_id)
        if user_id:
            filtered = True
            founds = founds.filter(user_id=user_id)

        if filtered:
            dicts = []
            for found in founds:
                the_dict = model_to_dict(found)
                the_dict['created_at'] = f"{found.created_at}"
                dicts.append(the_dict)
            return JsonResponse(build_dicts(dicts), status=200, safe=False)
        else:
            dicts = []
            for found in founds[:10]:
                the_dict = model_to_dict(found)
                the_dict['created_at'] = f"{found.created_at}"
                dicts.append(the_dict)
            return JsonResponse(build_dicts(dicts), status=200, safe=False)

def build_dicts(dicts):
    for dict in dicts:
        build_dict(dict)
    return dicts

def build_dict(the_dict: dict):
    if the_dict.get('org'):
        the_dict['org_id'] = the_dict['org']
        try:
            the_dict['org'] = model_to_dict(Org.objects.get(pk=the_dict['org_id']))
        except Exception as org_e:
            pass

    if the_dict.get('user'):
        the_dict['user_id'] = the_dict['user']
        try:
            user = User.objects.get(pk=the_dict['user_id'])
            user_dict = model_to_dict(user)
            group_dicts = []
            try:
                for group in user_dict.get('groups'):
                    group_dict = model_to_dict(group)
                    permission_dicts = []
                    try:
                        for permission in group_dict.get('permissions'):
                            permission_dict = model_to_dict(permission)
                            permission_dicts.append(permission_dict)
                    except Exception as permission_e:
                        pass
                    group_dict['permissions'] = permission_dicts
                    group_dicts.append(group_dict)
            except Exception as groups_e:
                pass
            user_permission_dicts = []
            try:
                for user_permission in user_dict.get("user_permissions"):
                    user_permission_dict = model_to_dict(user_permission)
                    user_permission_dict.append(user_permission_dict)
            except Exception as permission_e:
                pass
            user_dict['user_permissions'] = user_permission_dicts
            user_dict['groups'] = group_dicts
            the_dict['user'] = user_dict
        except Exception as user_e:
            pass

    return the_dict