from django.apps import AppConfig
from django.forms import model_to_dict


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        print(f"============================================================")
        print(f"""
                      .__                       _____.__        
        _____  ______ |__|   ____  ____   _____/ ____\__| ____  
        \__  \ \____ \|  | _/ ___\/  _ \ /    \   __\|  |/ ___\ 
         / __ \|  |_> >  | \  \__(  <_> )   |  \  |  |  / /_/  >
        (____  /   __/|__|  \___  >____/|___|  /__|  |__\___  / 
             \/|__|             \/           \/        /_____/  
        """)
        print(f"------------------------------------------------------------")

        self.confirmDefaultUser()
        self.confirmDefaultOrgs()
        self.confirmUserOrgs()
        self.confirmDefaultGroups()
        self.confirmDefaultPermissions()
        self.confirmDefaultGroupPermissions()

    def confirmUserOrgs(self):
        print(f"confirmUserOrgs()...")
        from api.models.user import UserOrg
        from api.models.org import Org
        from django.contrib.auth.models import User

        admin = User.objects.filter(username='jitguruadmin').first()

        orgCommunity = Org.objects.filter(name='jitguru:community').first()
        orgCommunityDict = model_to_dict(orgCommunity, fields=[field.name for field in orgCommunity._meta.fields])
        userOrgs = UserOrg.objects.filter(org_id=orgCommunityDict["id"], user_id=admin.id).first()
        if userOrgs is None:
            UserOrg.objects.create(user_id=admin.id, org_id=orgCommunityDict["id"])

        orgFacility = Org.objects.filter(name='jitguru:facility').first()
        orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
        userOrgs = UserOrg.objects.filter(org_id=orgFacilityDict["id"], user_id=admin.id).first()
        if userOrgs is None:
            UserOrg.objects.create(user_id=admin.id, org_id=orgFacilityDict["id"])

        orgMultifacility = Org.objects.filter(name='jitguru:multifacility').first()
        orgMultifacilityDict = model_to_dict(orgMultifacility, fields=[field.name for field in orgMultifacility._meta.fields])
        userOrgs = UserOrg.objects.filter(org_id=orgMultifacilityDict["id"], user_id=admin.id).first()
        if userOrgs is None:
            UserOrg.objects.create(user_id=admin.id, org_id=orgMultifacilityDict["id"])

    def confirmDefaultGroupPermissions(self):
        print(f"confirmDefaultGroupPermissions()...")
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission
        from django.contrib.auth.models import User
        admins = Group.objects.filter(name="admins").first()
        assign_org_to_self = Permission.objects.filter(codename="assign_org_to_self").first()
        admin = User.objects.filter(username="jitguruadmin").first()
        admins.permissions.add(assign_org_to_self)
        admin.groups.add(admins)

    def confirmDefaultPermissions(self):
        print(f"confirmDefaultPermissions()...")
        from django.contrib.auth.models import Permission
        found = Permission.objects.filter(codename="assign_org_to_self").first()
        if found is None:
            created = Permission.objects.create(codename="assign_org_to_self", content_type_id=17, name="Can assign org to self")
            if created is not None:
                print(f"created permission: assign_org_to_self")

    def confirmDefaultGroups(self):
        print(f"confirmDefaultGroups...")
        from django.contrib.auth.models import Group
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


    def confirmDefaultUser(self):
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

    def confirmDefaultOrgs(self):
        print(f"confirmDefaultOrgs...")
        from api.models.org import Org

        found = Org.objects.filter(name='jitguru:community').first()
        if found == None:
            created = Org.objects.create(name='jitguru:community')
            if created is not None:
                print(f"created org: {created.name}")
                created.description = "demonstrates distributed instruction and learning without a facility"
                created.save()

        found = Org.objects.filter(name='jitguru:facility').first()
        if found == None:
            created = Org.objects.create(name='jitguru:facility')
            if created is not None:
                print(f"created org: {created.name}")
                created.description = "demonstrates distributed instruction and learning centered in one physical faciliity"
                created.save()

        found = Org.objects.filter(name='jitguru:multifacility').first()
        if found == None:
            created = Org.objects.create(name='jitguru:multifacility')
            if created is not None:
                print(f"created org: {created.name}")
                created.description = "demonstrates distributed instruction and learning centered more than one physical faciliity"
                created.save()
