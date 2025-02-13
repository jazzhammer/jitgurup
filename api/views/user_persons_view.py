from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from api.models.person import Person
from api.models.user_person import UserPerson

@api_view(["POST", "GET", "DELETE"])
def user_persons(request, *args, **kwargs):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                person_id = request.data.get('person_id')
                if person_id:
                    person = Person.objects.get(pk=person_id)
                    if person:
                        created = UserPerson.objects.create(user=user, person=person)
                        return JsonResponse(model_to_dict(created), status=201, safe=False)
                    else:
                        return JsonResponse({"message": f"require person for user_person, found {person_id=}"}, status=400, safe=False)
                else:
                    return JsonResponse({"message": f"require person for user_person, found {person_id=}"}, status=400,
                                        safe=False)
            else:
                return JsonResponse({"message": f"require user for user_person, found {user_id=}"}, status=400,
                                    safe=False)
        else:
            return JsonResponse({"message": f"require user for user_person, found {user_id=}"}, status=400,
                                safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        person_id = request.GET.get('person_id')

        if id:
            try:
                found = UserPerson.objects.get(pk=id)
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as get_e:
                return JsonResponse({"message": f"error getting user_person for {id=}"}, status=400, safe=False)
        founds = UserPerson.objects.all()
        filtered = False
        if user_id:
            filtered = True
            founds = founds.filter(user_id=user_id)
        if person_id:
            filtered = True
            founds = founds.filter(person_id=person_id)
        if filtered:
            return JsonResponse([model_to_dict(found) for found in founds], status=200, safe=False)
        else:
            return JsonResponse({
                "message": "require query-limiting param, eg. user_id",
            }, status=404)

    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if not id:
            return JsonResponse({
                "error": f"require id to delete user_person, found {id=}"
            }, status=400, safe=False)
        else:
            found = UserPerson.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"user_person not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)


@api_view(['POST'])
def reset_tests(request, *args, **kwargs):
    User.objects.filter().exclude(username='jitguruadmin').delete()
    UserPerson.objects.all().delete()
    return JsonResponse({
        "message": "success",
        "deleted": "all"
    }, status=200)