import os

from django.apps import AppConfig
from django.forms import model_to_dict
from dotenv import load_dotenv
load_dotenv()


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        print(f"============================================================")
        print(f"""
                      .__                       _____.__
        _____  ______ |__|   ____  ____   _____/ ____\__| ____
        \__  \ \____ \|  | _/ ___\/  _ \ /    \   __\|  |/ ___| 
         / __ \|  |_> >  | \  \__(  <_> )   |  \  |  |  / /_/  >
        (____  /   __/|__|  \___  >____/|___|  /__|  |__\___  /
             \/|__|             \/           \/        /_____/
        """)
        print(f"------------------------------------------------------------")

        self.confirmDefaultUsers()
        # self.confirmDefaultOrgs()
        # self.confirmUserOrgs()
        # self.confirmDefaultGroups()
        # self.confirmDefaultPermissions()
        # self.confirmDefaultGroupPermissions()

    def confirmUserOrgs(self):
        print(f"confirmUserOrgs()...")
        from api.models.user_org import UserOrg
        from api.models.org import Org
        from django.contrib.auth.models import User
        from api.models.facility import Facility
        try:
            admin = User.objects.filter(username='jitguruadmin').first()

            orgCommunity = Org.objects.filter(name='jitguru org:community').first()
            if orgCommunity is None:
                orgCommunity = Org.objects.create(name='jitguru org:community')

            orgCommunityDict = model_to_dict(orgCommunity, fields=[field.name for field in orgCommunity._meta.fields])
            userOrgs = UserOrg.objects.filter(org_id=orgCommunityDict["id"], user_id=admin.id).first()
            if userOrgs is None:
                UserOrg.objects.create(user_id=admin.id, org_id=orgCommunityDict["id"])

            orgFacility = Org.objects.filter(name='jitguru org:1 facility').first()
            if orgFacility is None:
                orgFacility = Org.objects.create(name='jitguru org:1 facility')
            if orgFacility is not None:
                orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
                userOrgs = UserOrg.objects.filter(org_id=orgFacilityDict["id"], user_id=admin.id).first()
                if userOrgs is None:
                    userOrg = UserOrg.objects.create(user_id=admin.id, org_id=orgFacilityDict["id"])
                # create the one facility for this org. ergo... orgFacilityFacility
                orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
                facility = Facility.objects.filter(org_id=orgFacilityDict['id']).first()
                if facility is None:
                    facility = Facility.objects.create(org_id=orgFacilityDict['id'],name='jitguru facility: millhouse', description='singleton facility of jitguru org: facility')

            orgMultifacility = Org.objects.filter(name='jitguru org:multifacility').first()
            if orgMultifacility is None:
                orgMultifacility = Org.objects.create(name='jitguru org:multifacility')
            if orgMultifacility is not None:
                orgMultifacilityDict = model_to_dict(orgMultifacility, fields=[field.name for field in orgMultifacility._meta.fields])
                userOrgs = UserOrg.objects.filter(org_id=orgMultifacilityDict["id"], user_id=admin.id).first()
                if userOrgs is None:
                    UserOrg.objects.create(user_id=admin.id, org_id=orgMultifacilityDict["id"])
                # create the facilitys for this org.
                orgMultifacilityDict = model_to_dict(orgMultifacility, fields=[field.name for field in orgMultifacility._meta.fields])
                facilitys = Facility.objects.filter(org_id=orgMultifacilityDict['id'])
                if facilitys is None or len(facilitys) == 0:
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: henhouse', description='1/3 of multifacility')
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: woodshed', description='2/3 of multifacility')
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: hayshed', description='3/3 of multifacility')
        except Exception as e:
            print(f"unable to confirm user orgs: {e}")

    def confirmDefaultGroupPermissions(self):
        print(f"confirmDefaultGroupPermissions()...")
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission
        from django.contrib.auth.models import User
        try:
            admins = Group.objects.filter(name="admins").first()
            admin = User.objects.filter(username="jitguruadmin").first()

            assign_org_to_self = Permission.objects.filter(codename="assign_org_to_self").first()
            add_org = Permission.objects.filter(codename="add_org").first()
            add_facility = Permission.objects.filter(codename="add_facility").first()

            admins.permissions.add(assign_org_to_self)
            admins.permissions.add(add_org)
            admins.permissions.add(add_facility)

            admin.groups.add(admins)
        except Exception as e:
            print(f"unable to conrirm default group permissions: {e}")

    def confirmDefaultPermissions(self):
        print(f"confirmDefaultPermissions()...")
        from django.contrib.auth.models import Permission
        try:
            found = Permission.objects.filter(codename="assign_org_to_self").first()
            if found is None:
                created = Permission.objects.create(codename="assign_org_to_self", content_type_id=17, name="Can assign org to self")
                if created is not None:
                    print(f"created permission: assign_org_to_self")
        except Exception as e:
            print(f"unable to confirm default permissions: {e}")

    def confirmDefaultGroups(self):
        print(f"confirmDefaultGroups...")
        from django.contrib.auth.models import Group
        try:
            found = Group.objects.filter(name="admins").first()
            if found is None:
                try:
                    created = Group.objects.create(name="admins")
                    if created is not None:
                        print(f"created group: admins")
                    else:
                        print(f"unable to create group: admins")
                except:
                    print(f"error creating group: admins")
        except Exception as e:
            print(f"unable to confirm default groups: {e}")

    def create_common_user(self, username, email, password):
        environment = os.getenv('ENVIRONMENT')
        if environment == 'local':
            from django.contrib.auth.models import User
            created = User.objects.create_user(username, email, password)
            created.last_name = 'common'
            created.first_name = 'user'
            created.save()
            return created
        else:
            print(f"no common user available for environment: {environment}")
            return None

    def confirmDefaultUsers(self):
        print(f"confirmDefaultUsers...")
        from django.contrib.auth.models import User

        try:
            password = os.getenv('DEFAULT_PASSWORD')
            username = os.getenv('DEFAULT_USERNAME')
            print(f"{f"confirming user":32}: {username}")
            created = None
            try:
                found = User.objects.get(username=username)
                if not found:
                    print(f"{f"confirming user":32}: not found, creating...")
                    created = self.create_common_user(username, 'admin@jitguru.com', password)
                else:
                    print(f"{f"":32}: ok: {found.id}")
                    return
            except Exception as not_found_e:
                print(f"{f"confirming user":32}: not found, creating...")
                created = self.create_common_user(username, 'admin@jitguru.com', password)

            if created:
                print(f"{f"":32}: ok: {created.id}")
            else:
                print(f"{f"":32}: fail: for previous errors")

        except Exception as user_e:
            print(f"error confirming user: {username}: {user_e}")

        try:
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
        except Exception as e:
            print(f"unable to confirm default user: {e}")

        try:
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
        except Exception as e:
            print(f"unable to confirm default user: {e}")

    def confirmDefaultOrg(self, name, description):
        print(f"confirmDefaultOrg({name})...")
        from api.models.org import Org
        try:
            found = Org.objects.filter(name=name).first()
            if found == None:
                created = Org.objects.create(name=name)
                if created is not None:
                    print(f"created org: {created.name}")
                    created.description = description
                    created.save()
                else:
                    print(f"unable to create default org: {name}")
        except Exception as e:
            print(f"unable to confirm default org {name}: {e}")

    def confirmDefaultOrgs(self):
        print(f"confirmDefaultOrgs...")
        self.confirmDefaultOrg('jitguru:community', "demonstrates distributed instruction and learning without a facility")
        self.confirmDefaultOrg('jitguru:facility', "demonstrates distributed instruction and learning centered in one physical faciliity")
        self.confirmDefaultOrg('jitguru:multifacility', "demonstrates distributed instruction and learning centered more than one physical faciliity")
