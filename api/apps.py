import django
from django.apps import AppConfig

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
        from .models import Org

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
