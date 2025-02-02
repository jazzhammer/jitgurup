from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view

from api.models.crew import Crew
from api.models.facility import Facility
from api.models.meetup import Meetup
from api.models.meetup_spot import MeetupSpot
from api.models.meetup_template import MeetupTemplate
from api.models.org import Org


@api_view(["POST", "GET", "PUT", "DELETE"])
def meetup(request, **kwargs):
    if request.method == 'POST':
        start_at: str = request.data.get('start_at')
        # in minutes
        duration: int = request.data.get('duration')
        if not duration or duration < 5:
            duration = 5

        # at least copied from the meetup template
        # likely modified by the guru hosting the meetup
        name = request.data.get("name")
        if not name:
            return JsonResponse({"message": f"require name for meetup, found {name}"}, status=400, safe=False)

        # for larger organizations and more complex learning environments,
        # these fields will likely be filled.
        # by default, they should be optional
        meetup_template_id = request.data.get('meetup_template_id')
        org_id = request.data.get('org_id')
        facility_id = request.data.get('facility_id')
        meetup_spot_id = request.data.get('meetup_spot_id')
        crew_id = request.data.get('crew_id')

        try:
            start_at_dt = parse_datetime(start_at)
        except:
            return JsonResponse({
                'error': f"require valid start_at for meetup, found {start_at=}"
            }, status=400, safe=False)

        created = Meetup.objects.create(
            start_at=start_at_dt,
            duration=duration,
            name=name
        )

        if meetup_template_id:
            created.meetup_template_id = meetup_template_id
        if org_id:
            created.org = Org.objects.get(pk=org_id)
        if facility_id:
            created.facility = Facility.objects.get(pk=facility_id)
        if meetup_spot_id:
            created.meetup_spot = MeetupSpot.objects.get(pk=meetup_spot_id)
        if crew_id:
            created.crew = Crew.objects.get(pk=crew_id)
        if name:
            created.name = name
        created.save()

        return JsonResponse(model_to_dict(created), status=201, safe=False)

    if request.method == 'GET':
        id = request.data.get('id')
        topic_name = request.data.get('topic_name')

        if id:
            try:
                found = Meetup.objects.get(pk=id)
            except:
                return JsonResponse({
                    'error': f"no meetup found for {id=}"
                }, status=404, safe=False)
            return JsonResponse({
                "message": "success",
                "matched": [model_to_dict(found)]
            }, status=200, safe=False)

        if topic_name and len(topic_name.strip()) > 0:
            pass

        filtered = False
        founds = Meetup.objects.filter(deleted=False)
        name = request.GET.get('name')
        if name:
            filtered = True
            founds = founds.filter(name__icontains=name)
        start_at_from = request.GET.get('start_at_from')
        if start_at_from:
            filtered = True
            founds = founds.filter(start_at__gte=start_at_from)
        start_at_to = request.GET.get('start_at_to')
        if start_at_to:
            filtered = True
            founds = founds.filter(start_at__lt=start_at_to)
        duration_from = request.GET.get('duration_from')
        if duration_from:
            filtered = True
            founds = founds.filter(duration__gt=duration_from)
        duration_to = request.GET.get('duration_to')
        if duration_to:
            filtered = True
            founds = founds.filter(duration__lt=duration_to)
        meetup_template_id = request.GET.get('meetup_template_id')
        if meetup_template_id:
            filtered = True
            founds = founds.filter(meetup_template_id=meetup_template_id)
        org_id = request.GET.get('org_id')
        if org_id:
            filtered = True
            founds = founds.filter(org_id=org_id)
        facility_id = request.GET.get('facility_id')
        if facility_id:
            filtered = True
            founds = founds.filter(facility_id=facility_id)
        meetup_spot_id = request.GET.get('meetup_spot_id')
        if meetup_spot_id:
            filtered = True
            founds = founds.filter(meetup_spot_id=meetup_spot_id)
        crew_id = request.GET.get('crew_id')
        if crew_id:
            filtered = True
            founds = founds.filter(crew_id=crew_id)

        if filtered:
            return JsonResponse(model_to_dict(founds), status=200, safe=False)
        else:
            return JsonResponse({
                                    "message": f"require combination of name | start_at | duration | meetup_template | org | facility | meetup_spot | crew for search of meetup"},
                                status=400, safe=False)

    if request.method == 'PUT':
        id = request.data.get('id')
        name = request.data.get('name')
        start_at = request.data.get('start_at')
        meetup_template_id = request.data.get('meetup_template_id')
        org_id = request.data.get('org_id')
        facility_id = request.data.get('facility_id')
        meetup_spot_id = request.data.get('meetup_spot_id')
        crew_id = request.data.get('crew_id')

        found = None
        if id:
            try:
                found = Meetup.objects.get(pk=id)
            except:
                return JsonResponse({
                    'error': f"no meetup found for {id=}"
                }, status=404, safe=False)
        if name:
            found.name = name
        if start_at:
            found.start_at = start_at
        duration = request.GET.get('duration')
        if duration:
            found.duration = duration
        if meetup_template_id:
            found.meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
        if org_id:
            found.org = Org.objects.get(pk=org_id)
        if facility_id:
            found.facility = Facility.objects.get(pk=facility_id)
        if meetup_spot_id:
            found.meetup_spot = MeetupTemplate.objects.get(pk=meetup_spot_id)
        if crew_id:
            found.crew = Crew.objects.get(pk=crew_id)
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'DELETE':
        id: str = request.GET.get('id')
        erase = request.GET.get('erase')
        if id and len(id.strip()) > 0:
            found = Meetup.objects.get(pk=id)
            if erase:
                found.delete()
            else:
                found.deleted = True
                found.save()
            return JsonResponse(model_to_dict(found), status=200, safe=False)
        else:
            return JsonResponse({
                "error": f"unable to update meetup for {id=}"
            }, status=400, safe=False)