from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models.crew import Crew
from api.models.meetup_role import MeetupRole, GURU
from api.models.person import Person
from api.models.signup import Signup
from api.models.meetup import Meetup

@api_view(['GET'])
def signup(request, signup_id):
    found = Signup.objects.get(id=signup_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    Signup.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def signups(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = Signup.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"signup not found for delete {id=}",
            }, status=404, safe=False)
        meetup_role = None
        try:
            meetup_role = MeetupRole.objects.get(pk=found.meetup_role_id)
        except Exception as meetup_role_e:
            pass
        if meetup_role:
            if meetup_role.name == GURU:
                return JsonResponse({"message": f"unable to delete signup for role: GURU"}, status=400, safe=False)

        found.deleted = True
        found.save()
        if erase:
            found.delete()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        person_id = request.data.get('person_id')
        meetup_role_id = request.data.get('meetup_role_id')
        crew_id = request.data.get('crew_id')
        created_by_id = request.data.get('created_by_id')

        try:
            found = Signup.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"signup not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = Signup.objects.all()
        dupes.exclude(id=id)
        if person_id:
            person_id = int(person_id)
            try:
                person = Person.objects.get(pk=person_id)
                found.person = person
            except:
                return JsonResponse({
                    "error": f"require valid person_id to update signup, found {person_id=}",
                }, status=400, safe=False)

        if meetup_role_id:
            meetup_role_id = int(meetup_role_id)
            try:
                meetup_role = MeetupRole.objects.get(pk=meetup_role_id)
                found.meetup_role = meetup_role
            except:
                return JsonResponse({
                    "error": f"require valid meetup_role_id to update signup, found {meetup_role_id=}",
                }, status=400, safe=False)

        if crew_id:
            crew_id = int(crew_id)
            try:
                crew = Crew.objects.get(pk=crew_id)
                found.crew = crew
            except:
                return JsonResponse({
                    "error": f"require valid crew_id to update signup, found {crew_id=}",
                }, status=400, safe=False)

        found.deleted = False
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        person_id: int = request.data.get('person_id')
        meetup_role_id: int = request.data.get('meetup_role_id')
        crew_id: int = request.data.get('crew_id')
        created_by_id: int = request.data.get('created_by_id')

        try:
            meetup_role = MeetupRole.objects.get(pk=meetup_role_id)
            person = Person.objects.get(pk=person_id)
            crew = Crew.objects.get(pk=crew_id)
        except Exception as save_e:
            return JsonResponse({
                "error": f"require meetup role, person, crew for signup {crew_id=}, {person_id=}, {meetup_role_id=}: {save_e}",
            }, status=400, safe=False)

        dupes = Signup.objects.filter(crew_id=crew_id, meetup_role_id=meetup_role_id, person_id=person_id)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False

                    dupe.save()
                    return JsonResponse(model_to_dict(dupe), status=201, safe=False)

        created = Signup.objects.create(
            person=person,
            meetup_role=meetup_role,
            crew=crew,
            created_by_id=created_by_id
        )
        return JsonResponse(model_to_dict(created), status=201, safe=False)


    if request.method == 'GET':
        person_id = request.GET.get('person_id')
        meetup_id = request.GET.get('meetup_id')
        created_by_id = request.GET.get('created_by_id')
        meetup_role_id = request.GET.get('meetup_role_id')
        crew_id = request.GET.get('crew_id')
        founds = Signup.objects.all()
        filtered = False
        query = f"""
                select
                    api_signup.*
                from
                    api_crew
                ,   api_signup
                where 1 = 1 
                and api_signup.crew_id = api_crew.id            
            """
        raw = False
        if meetup_role_id:
            raw = True
            query = f"{query}\nand api_signup.meetup_role_id = {meetup_role_id}"
        if crew_id:
            raw = True
            query = f"{query}\nand api_signup.crew_id = {crew_id}"
        if meetup_id:
            raw = True
            query = f"{query}\nand api_crew.meetup_id = {meetup_id}"
        if person_id:
            raw = True
            query = f"{query}\nand api_signup.person_id = {person_id}"
        if created_by_id:
            raw = True
            query = f"{query}\nand api_signup.created_by_id = {created_by_id}"

        if raw:
            founds = Signup.objects.raw(query)
        else:
            founds = Signup.objects.all()[:10]
        dicts = build_dicts([model_to_dict(instance) for instance in founds])
        return JsonResponse(dicts, status=200, safe=False)

def build_dicts(dicts):
    for dict in dicts:
        if dict.get('meetup_role'):
            dict['meetup_role_id'] = dict['meetup_role']
            meetup_role = MeetupRole.objects.get(pk=dict['meetup_role_id'])
            dict['meetup_role'] = model_to_dict(meetup_role)
        if dict.get('person'):
            dict['person_id'] = dict['person']
            person = Person.objects.get(pk=dict['person_id'])
            dict['person'] = model_to_dict(person)
        if dict.get('crew'):
            dict['crew_id'] = dict['crew']
            crew = Crew.objects.get(pk=dict['crew_id'])
            dict['crew'] = model_to_dict(crew)
        if dict.get('create_by'):
            dict['created_by_id'] = dict['created_by']
            user = User.objects.get(pk=dict['created_by_id'])
            dict['created_by'] = model_to_dict(user)
    return dicts