from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view


from api.models.crew_template import CrewTemplate
from api.models.facility import Facility
from api.models.focus import Focus
from api.models.meetup_spot import MeetupSpot
from api.models.meetup_template import MeetupTemplate
from api.models.org import Org
from api.models.subject import Subject


@api_view(['GET'])
def meetup_template(request, meetup_template_id):
    found = MeetupTemplate.objects.get(id=meetup_template_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def meetup_templates(request, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if id:
            try:
                found = MeetupTemplate.objects.get(pk=id)
            except:
                return JsonResponse({
                    "error": f"meetup_template not found for {id=}",
                }, status=404)
            found.deleted = True
            found.save()
            return JsonResponse({
                "message": "success",
                "deleted": model_to_dict(found)
            }, status=200)
        else:
            return JsonResponse({
                "error": f"meetup_template not found for {id=}",
            }, status=404)

    if request.method == 'PUT':
        id = request.data.get('id')
        if not id:
            return JsonResponse({
                "error": f"meetup_template not found for {id=}",
            }, status=404)

        try:
            found = MeetupTemplate.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"meetup_template not found for {id=}",
            }, status=404)

        name = request.data.get('name')
        org_id: int = request.data.get('org_id')
        facility_id: int = request.data.get('facility_id')
        meetup_spot_id: int = request.data.get('meetup_spot_id')
        crew_template_id: int = request.data.get('crew_template_id')
        focus_id: int = request.data.get('focus_id')
        subject_id: int = request.data.get('subject_id')
        work_in_progress: bool = request.data.get('work_in_progress')

        dupes: QuerySet = MeetupTemplate.objects.all().exclude(id=id)
        if name and len(name.strip()) > 0:
            dupes = dupes.filter(name__iexact=name)
        else:
            return JsonResponse({
                "error": f"name required to find meetup_template, found: {name=}",
            }, status=400)
        if org_id:
            dupes = dupes.filter(org_id=org_id)
        if facility_id:
            dupes = dupes.filter(facility_id=facility_id)
        if meetup_spot_id:
            dupes = dupes.filter(meetup_spot_id=meetup_spot_id)
        if crew_template_id:
            dupes = dupes.filter(crew_template_id=crew_template_id)
        if focus_id:
            dupes = dupes.filter(focus_id=focus_id)
        if subject_id:
            dupes = dupes.filter(subject_id=subject_id)
        if work_in_progress is not None:
            dupes = dupes.filter(work_in_progress=str(work_in_progress).strip().lower() == 'true')
        if dupes.count() > 0:
            found = dupes.first()
            found.deleted = False
            found.save()
            return JsonResponse({
                "message": "success",
                "updated": model_to_dict(found)
            }, status=200)
        else:
            updated = MeetupTemplate.objects.get(pk=id)
            if org_id:
                updated.org = Org.objects.get(pk=org_id)
            if facility_id:
                updated.facility = Facility.objects.get(pk=facility_id)
            if meetup_spot_id:
                updated.meetup_spot = MeetupSpot.objects.get(pk=meetup_spot_id)
            if crew_template_id:
                updated.crew_template = CrewTemplate.objects.get(pk=crew_template_id)
            if focus_id:
                updated.focus = CrewTemplate.objects.get(pk=focus_id)
            if subject_id:
                updated.subject = CrewTemplate.objects.get(pk=subject_id)
            if work_in_progress is not None:
                updated.work_in_progress = str(work_in_progress).lower().strip() == 'true'
            if name:
                updated.name = name
            updated.save()
            return JsonResponse({
                "message": "success",
                "updated": model_to_dict(updated)
            }, status=201)

    if request.method == 'POST':
        name = request.data.get('name')
        if not name or len(name.strip()) == 0:
            return JsonResponse({
                "error": f"name required for new meetup_template, found: {name=}",
            }, status=400)

        org_id: int = request.data.get('org_id')
        try:
            org = Org.objects.get(id=org_id)
        except:
            return JsonResponse({
                "error": f"org required for new meetup_template, found: {org_id=}",
            }, status=400)
        facility_id: int = request.data.get('facility_id')
        meetup_spot_id: int = request.data.get('meetup_spot_id')
        crew_template_id: int = request.data.get('crew_template_id')
        focus_id: int = request.data.get('focus_id')
        subject_id: int = request.data.get('subject_id')
        work_in_progress: bool = request.data.get('work_in_progress')

        dupes: QuerySet = MeetupTemplate.objects.filter(deleted=False, org_id=org_id)
        if name and len(name.strip()) > 0:
            dupes = dupes.filter(name__iexact=name)
        else:
            return JsonResponse({
                "error": f"name required for new meetup_template, found: {name=}",
            }, status=404)
        if facility_id:
            dupes = dupes.filter(facility_id=facility_id)
        if meetup_spot_id:
            dupes = dupes.filter(meetup_spot_id=meetup_spot_id)
        if dupes.count() > 0:
            found = dupes.first()
            try:
                focus = Focus.objects.get(pk=focus_id)
            except:
                pass
            try:
                subject = Subject.objects.get(pk=subject_id)
            except:
                pass
            if focus:
                found.focus = focus
            if subject:
                found.subject = subject
            if work_in_progress is not None:
                found.work_in_progress = str(work_in_progress).lower().strip() == 'true'
            found.deleted = False
            found.save()
            return JsonResponse({
                "message": "success",
                "created": model_to_dict(found)
            }, status=201)
        else:
            created = MeetupTemplate.objects.create(name=name)
            if org_id:
                created.org = Org.objects.get(pk=org_id)
            if facility_id:
                created.facility = Facility.objects.get(pk=facility_id)
            if meetup_spot_id:
                created.meetup_spot = MeetupSpot.objects.get(pk=meetup_spot_id)
            if crew_template_id:
                created.crew_template = CrewTemplate.objects.get(pk=crew_template_id)
            if focus_id:
                created.focus = Focus.objects.get(pk=focus_id)
            if subject_id:
                created.subject = Subject.objects.get(pk=subject_id)
            if work_in_progress is not None:
                created.work_in_progress = str(work_in_progress).lower().strip() == 'true'
            created.save()
            return JsonResponse({
                "message": "success",
                "created": model_to_dict(created)
            }, status=201)


    if request.method == 'GET':
        name = request.GET.get('name')
        org_id = request.GET.get('org_id')
        facility_id = request.GET.get('facility_id')
        meetup_spot_id = request.GET.get('meetup_spot_id')
        focus_id = request.GET.get('focus_id')
        subject_id = request.GET.get('subject_id')
        work_in_progress = request.GET.get('work_in_progress')
        founds: QuerySet = MeetupTemplate.objects.filter(deleted=False)
        filtered = False
        if name:
            filtered = True
            founds = founds.filter(name_iexact=name)
        if org_id:
            filtered = True
            founds = MeetupTemplate.objects.filter(org_id=org_id)
        if facility_id:
            filtered = True
            founds = MeetupTemplate.objects.filter(facility_id=facility_id)
        if meetup_spot_id:
            filtered = True
            founds = MeetupTemplate.objects.filter(meetup_spot_id=meetup_spot_id)
        if focus_id:
            filtered = True
            founds = MeetupTemplate.objects.filter(focus_id=focus_id)
        if subject_id:
            filtered = True
            founds = MeetupTemplate.objects.filter(subject_id=subject_id)
        if work_in_progress is not None:
            filtered = True
            founds = MeetupTemplate.objects.filter(work_in_progress=str(work_in_progress).lower().strip() == 'true')
        if not filtered:
            founds = MeetupTemplate.objects.all().filter(deleted=False)[:10]
        return JsonResponse({
            "message": "success",
            "matched": [model_to_dict(found) for found in founds]
        }, status=200)
