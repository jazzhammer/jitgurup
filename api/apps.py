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