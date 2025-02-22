from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.meetup_calculation import MeetupCalculation
from api.models.org import Org

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def meetup_calculations(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = MeetupCalculation.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"meetup_calculation not found for deletion {id=}: {get_e}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(build(model_to_dict(found)), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        pupil_count = request.data.get("pupil_count")
        guru_count = request.data.get("guru_count")
        daily_meetup_interval_length = request.data.get("daily_meetup_interval_length")
        intermeetup_transition = request.data.get("intermeetup_transition")
        max_meetups_per_guru_per_day = request.data.get("max_meetups_per_guru_per_day")
        total_guru_minutes_per_day = request.data.get("total_guru_minutes_per_day")
        max_pupil_meetups_per_day = request.data.get("max_pupil_meetups_per_day")
        minimum_pupil_meetups_per_day = request.data.get("minimum_pupil_meetups_per_day")
        org_id: int = request.data.get('org_id')
        found = None
        if id:
            try:
                found = MeetupCalculation.objects.get(pk=id)
            except:
                return JsonResponse({
                    "error": f"meetup_calculation not found for update {id=}",
                }, status=404, safe=False)
        if org_id:
            try:
                org = Org.objects.get(pk=org_id)
            except:
                return JsonResponse({
                    "error": f"require valid org_id to update org_id, found {org_id=}",
                }, status=400, safe=False)
            found.org = org
        if pupil_count:
            found.pupil_count = pupil_count
        if guru_count:
            found.guru_count = guru_count
        if daily_meetup_interval_length:
            found.daily_meetup_interval_length = daily_meetup_interval_length
        if intermeetup_transition:
            found.intermeetup_transition = intermeetup_transition
        if max_meetups_per_guru_per_day:
            found.max_meetups_per_guru_per_day = max_meetups_per_guru_per_day
        if total_guru_minutes_per_day:
            found.total_guru_minutes_per_day = total_guru_minutes_per_day
        if max_pupil_meetups_per_day:
            found.max_pupil_meetups_per_day = max_pupil_meetups_per_day
        if minimum_pupil_meetups_per_day:
            found.minimum_pupil_meetups_per_day = minimum_pupil_meetups_per_day

        found.save()

        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        pupil_count = request.data.get("pupil_count")
        guru_count = request.data.get("guru_count")
        daily_meetup_interval_length = request.data.get("daily_meetup_interval_length")
        intermeetup_transition = request.data.get("intermeetup_transition")
        max_meetups_per_guru_per_day = request.data.get("max_meetups_per_guru_per_day")
        total_guru_minutes_per_day = request.data.get("total_guru_minutes_per_day")
        max_pupil_meetups_per_day = request.data.get("max_pupil_meetups_per_day")
        minimum_pupil_meetups_per_day = request.data.get("minimum_pupil_meetups_per_day")
        org_id = request.data.get("org_id")

        created = MeetupCalculation.objects.create()

        if org_id:
            try:
                org = Org.objects.get(pk=org_id)
                created.org = org
            except Exception as org_e:
                return JsonResponse({"message": f"require valid org if org specified, found {org_id=}"}, status=400, safe=False)

        if pupil_count is not None:
            created.pupil_count = pupil_count
        if guru_count is not None:
            created.guru_count = guru_count
        if daily_meetup_interval_length is not None:
            created.daily_meetup_interval_length = daily_meetup_interval_length
        if intermeetup_transition is not None:
            created.intermeetup_transition = intermeetup_transition
        if max_meetups_per_guru_per_day is not None:
            created.max_meetups_per_guru_per_day = max_meetups_per_guru_per_day
        if total_guru_minutes_per_day is not None:
            created.total_guru_minutes_per_day = total_guru_minutes_per_day
        if max_pupil_meetups_per_day is not None:
            created.max_pupil_meetups_per_day = max_pupil_meetups_per_day
        if minimum_pupil_meetups_per_day is not None:
            created.minimum_pupil_meetups_per_day = minimum_pupil_meetups_per_day

        created.save()
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = MeetupCalculation.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no meetup_calculation found for {id=}'
                }, status=404, safe=False)
        org_id = request.GET.get('org_id')
        founds = MeetupCalculation.objects.all()
        filtered = False
        if org_id:
            filtered = True
            founds = founds.filter(org_id=org_id)
        if not filtered:
            founds = MeetupCalculation.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(meetup_calculation_dict: dict):
    org_id = meetup_calculation_dict.get('org')
    meetup_calculation_dict['org_id'] = org_id
    try:
        org = Org.objects.get(pk=org_id)
        meetup_calculation_dict['org'] = model_to_dict(org)
    except Exception as org_e:
        pass
    return meetup_calculation_dict