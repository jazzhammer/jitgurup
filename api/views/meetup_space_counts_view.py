from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.meetup_space_count import MeetupSpaceCount
from api.models.meetup_calculation import MeetupCalculation

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def meetup_space_counts(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        erase = request.GET.get('erase')
        try:
            found = MeetupSpaceCount.objects.get(pk=id)
        except Exception as get_e:
            return JsonResponse({
                "error": f"meetup_space_count not found for update {id=}: {get_e}",
            }, status=404, safe=False)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(build(model_to_dict(found)), status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        max_persons: str = request.data.get('max_persons')
        count: str = request.data.get('count')
        meetup_calculation_id: int = request.data.get('meetup_calculation_id')
        found = None
        try:
            found = MeetupSpaceCount.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"meetup_space_count not found for update {id=}",
            }, status=404, safe=False)
        dupes: QuerySet = MeetupSpaceCount.objects.all()
        dupes.exclude(id=id)
        if max_persons:
            if len(max_persons.strip()) <= 0:
                return JsonResponse({
                    "error": f"require max_persons",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(max_persons=max_persons)
        if meetup_calculation_id:
            try:
                meetup_calculation = MeetupCalculation.objects.get(pk=meetup_calculation_id)
                found.meetup_calculation = meetup_calculation
            except:
                return JsonResponse({
                    "error": f"require valid meetup_calculation_id to update meetup_calculation_id, found {meetup_calculation_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(meetup_calculation_id=meetup_calculation_id)
        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already meetup_space_count {max_persons=} for {meetup_calculation_id=}",
            }, status=400, safe=False)
        if count:
            if len(count.strip()) <= 0:
                count = count.strip()
                return JsonResponse({
                    "error": f"require non blank count if provided",
                }, status=400, safe=False)
        found.max_persons = max_persons
        found.count = count
        found.meetup_calculation = meetup_calculation
        found.deleted = False
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        max_persons: str = request.data.get('max_persons')
        count: str = request.data.get('count')
        meetup_calculation_id: str = request.data.get('meetup_calculation_id')
        dupes: QuerySet = MeetupSpaceCount.objects.all()
        if max_persons:
            if len(max_persons.strip()) <= 0:
                return JsonResponse({
                    "error": f"require max_persons",
                }, status=400, safe=False)
            else:
                dupes = dupes.filter(max_persons__iexact=max_persons.strip())
        else:
            return JsonResponse({
                "error": f"meetup_space_count requires max_persons, found {max_persons=}",
            }, status=400, safe=False)

        if meetup_calculation_id:
            try:
                meetup_calculation = MeetupCalculation.objects.get(pk=meetup_calculation_id)
            except:
                return JsonResponse({
                    "error": f"require valid meetup_calculation_id to update meetup_calculation_id, found {meetup_calculation_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(meetup_calculation_id=meetup_calculation_id)
        else:
            return JsonResponse({
                "error": f"meetup_space_count requires max_persons, found {max_persons=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse(build(model_to_dict(dupe)), status=201, safe=False)
        created = MeetupSpaceCount.objects.create(max_persons=max_persons, meetup_calculation=meetup_calculation, count=count)
        return JsonResponse(build(model_to_dict(created)), status=201, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = MeetupSpaceCount.objects.get(pk=id)
                return JsonResponse([build(model_to_dict(found))], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no meetup_space_count found for {id=}'
                }, status=404, safe=False)
        max_persons = request.GET.get('max_persons')
        meetup_calculation_id = request.GET.get('meetup_calculation_id')
        founds = MeetupSpaceCount.objects.all()
        filtered = False
        if max_persons is not None:
            if len(max_persons.strip()) > 0:
                filtered = True
                founds = MeetupSpaceCount.objects.filter(max_persons__icontains=max_persons)
        if meetup_calculation_id:
            filtered = True
            founds = founds.filter(meetup_calculation_id=meetup_calculation_id)
        if not filtered:
            founds = MeetupSpaceCount.objects.all()[:10]
        return JsonResponse([build(model_to_dict(instance)) for instance in founds], status=200, safe=False)

def build(meetup_space_count: dict):
    meetup_calculation_id = meetup_space_count.get('meetup_calculation')
    meetup_space_count['meetup_calculation_id'] = meetup_calculation_id
    try:
        meetup_calculation = MeetupCalculation.objects.get(pk=meetup_calculation_id)
        meetup_space_count['meetup_calculation'] = model_to_dict(meetup_calculation)
    except Exception as meetup_calculation_e:
        pass
    return meetup_space_count