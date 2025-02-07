from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from api.models.facility import Facility
from api.models.meetup_role import MeetupRole
from api.models.user_facility_role import UserFacilityRole


@api_view(["POST", "GET", "DELETE"])
def facility_roles(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                facility_id = request.data.get('facility_id')
                if facility_id:
                    facility = Facility.objects.get(pk=facility_id)
                    if facility:
                        meetup_role_id = request.data.get('meetup_role_id')
                        if meetup_role_id:
                            meetup_role = MeetupRole.objects.get(pk=meetup_role_id)
                            if meetup_role:
                                created = UserFacilityRole.objects.create(
                                    user=user,
                                    facility=facility,
                                    meetup_role=meetup_role
                                )
                                return JsonResponse(model_to_dict(created), status=201, safe=False)
                        else:
                            return JsonResponse({"message": f"require meetup_role for facility_meetup_role, found {meetup_role_id=}"}, status=400, safe=False)
                    else:
                        return JsonResponse({"message": f"require facility for facility_meetup_role, found {facility_id=}"}, status=400, safe=False)
                else:
                    return JsonResponse({"message": f"require facility for facility_meetup_role, found {facility_id=}"}, status=400,
                                        safe=False)
            else:
                return JsonResponse({"message": f"require user for facility_meetup_role, found {user_id=}"}, status=400,
                                    safe=False)
        else:
            return JsonResponse({"message": f"require user for facility_meetup_role, found {user_id=}"}, status=400,
                                safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        facility_id = request.GET.get('facility_id')
        meetup_role_id = request.GET.get('meetup_role_id')
        if id:
            try:
                found = Facility.objects.get(pk=id)
                return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as get_e:
                return JsonResponse({"message": f"error getting facility for {id=}"}, status=400, safe=False)
        founds = Facility.objects.all()
        filtered = False
        if user_id:
            filtered = True
            founds = founds.filter(user_id=user_id)
        if facility_id:
            filtered = True
            founds = founds.filter(facility_id=facility_id)
        if meetup_role_id:
            filtered = True
            founds = founds.filter(meetup_role_id=meetup_role_id)
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
                "error": f"require id to delete facility, found {id=}"
            }, status=400, safe=False)
        else:
            found = Facility.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"facility not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)

