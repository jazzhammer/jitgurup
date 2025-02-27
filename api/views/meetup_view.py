from datetime import datetime

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models.crew import Crew
from api.models.facility import Facility
from api.models.meetup import Meetup
from api.models.meetup_role import MeetupRole
from api.models.meetup_spot import MeetupSpot
from api.models.meetup_template import MeetupTemplate
from api.models.org import Org
from api.models.person import Person
from api.models.signup import Signup
from api.models.subject import Subject
from api.models.topic import Topic


@api_view(["POST", "GET", "PUT", "DELETE"])
def meetup(request, **kwargs):
    if request.method == 'POST':
        meetup_role_id = request.data.get('meetup_role_id')
        user_id = request.data.get('user_id')
        topic_id = request.data.get('topic_id')
        person = None
        if user_id:
            try:
                person = Person.objects.get(user_id=user_id)
            except Exception as person_e:
                pass

        # expect utc string,
        # store as utc integer
        utc = request.data.get('utc')
        start_at = None
        start_at_unix = None
        if utc:
            # expecting format: 2025-02-11T13:15:00.302Z
            utc = utc[0:-5]
            start_at = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S")
            start_at_unix = start_at.timestamp()
        # in minutes
        duration = request.data.get('duration')
        if not duration:
            duration = 5
        else:
            duration = int(duration)

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
        crew = None

        created = Meetup.objects.create(
            start_at=start_at,
            start_at_unix=start_at_unix,
            duration=duration,
            name=name
        )
        if start_at:
            created.year = start_at.year,
            created.month = start_at.month,  # jan = 1
            created.dom = start_at.day,
            created.hour = start_at.hour,
            created.minute = start_at.minute
            created.save()

        if meetup_template_id:
            created.meetup_template_id = meetup_template_id

        if org_id:
            created.org = Org.objects.get(pk=org_id)

        if facility_id:
            created.facility = Facility.objects.get(pk=facility_id)

        if meetup_spot_id:
            created.meetup_spot = MeetupSpot.objects.get(pk=meetup_spot_id)

        if crew_id:
            crew = Crew.objects.get(pk=crew_id)
        else:
            crew = Crew.objects.create(name=created.id, meetup=created)

        if topic_id:
            topic = Topic.objects.get(pk=topic_id)
            created.topic = topic
            created.save()

        if name:
            created.name = name
        # crew is not a property of meetup
        # meetup is a property of crew
        # created.crew = crew
        # ensure we have a signup for the person if there is a person
        # created.save()
        if person:
            created_by = User.objects.get(pk=user_id)
            meetup_role = None
            if meetup_role_id:
                try:
                    meetup_role = MeetupRole.objects.get(pk=meetup_role_id)
                except Exception as meetup_role_e:
                    pass

            signup = Signup.objects.create(
                created_by=created_by,
                meetup_role=meetup_role,
                crew=crew,
                person=person
            )

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
            return JsonResponse([model_to_dict(found)], status=200, safe=False)

        if topic_name and len(topic_name.strip()) > 0:
            pass

        utc_start = request.GET.get('utc_start')
        utc_finish = request.GET.get('utc_finish')
        user_id = request.GET.get('user_id')
        meetup_role_id = request.GET.get('meetup_role_id')

        if utc_start and utc_finish:
            # expecting format: 2025-02-11T13:15:00.302Z
            utc_start = utc_start[0:-5]
            start = datetime.strptime(utc_start, "%Y-%m-%dT%H:%M:%S")
            start_unix = start.timestamp()

            utc_finish = utc_finish[0:-5]
            finish = datetime.strptime(utc_finish, "%Y-%m-%dT%H:%M:%S")
            finish_unix = finish.timestamp()
            print(f"meetups search for {start} -> {finish}")
            query = f"""
                select 
                    api_meetup.* 
                from 
                    api_meetup,
                    api_crew,
                    api_signup,
                    api_person
                where 
                    api_crew.meetup_id = api_meetup.id
                and api_signup.crew_id = api_crew.id
                and api_signup.person_id = api_person.id
                and api_meetup.start_at >= '{start}'
                and api_meetup.start_at <  '{finish}'
            """
            if user_id:
                query += f"\nand api_person.user_id = {user_id}"
            if meetup_role_id:
                query += f"\nand api_signup.meetup_role_id = {meetup_role_id}"

            founds = Meetup.objects.raw(query)
            dicts = build_dicts([model_to_dict(found) for found in founds])
            return JsonResponse(dicts, status=200, safe=False)

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

        topic_id = request.GET.get('topic_id')
        if topic_id:
            filtered = True
            founds = founds.filter(topic_id=topic_id)

        facility_id = request.GET.get('facility_id')
        if facility_id:
            filtered = True
            founds = founds.filter(facility_id=facility_id)

        meetup_spot_id = request.GET.get('meetup_spot_id')
        if meetup_spot_id:
            filtered = True
            founds = founds.filter(meetup_spot_id=meetup_spot_id)

        # crew is not a property of meetup.
        # meetup is a property of crew
        # crew_id = request.GET.get('crew_id')
        # if crew_id:
        #     filtered = True
        #     founds = founds.filter(crew_id=crew_id)

        if filtered:

            dicts = build_dicts([model_to_dict(found) for found in founds])

            return JsonResponse(dicts, status=200, safe=False)
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

def build_dicts(dicts):
    for dict in dicts:
        if dict.get('org'):
            dict['org_id'] = dict['org']
            try:
                dict['org'] = model_to_dict(Org.objects.get(pk=dict['org_id']))
            except Exception as org_e:
                pass

        if dict.get('topic'):
            dict['topic_id'] = dict['topic']
            try:
                topic = Topic.objects.get(pk=dict['topic_id'])
                subject = Subject.objects.get(pk=topic.subject_id)
                topic_dict = model_to_dict(topic)
                topic_dict['subject_id'] = topic_dict['subject']
                topic_dict['subject'] = model_to_dict(subject)
                dict['topic'] = topic_dict
            except Exception as topic_e:
                pass

        if dict.get('facility'):
            dict['facility_id'] = dict['facility']
            try:
                dict['facility'] = model_to_dict(Facility.objects.get(pk=dict['facility_id']))
            except Exception as facility_e:
                pass


        if dict.get('meetup_spot'):
            dict['meetup_spot_id'] = dict['meetup_spot']
            try:
                dict['meetup_spot'] = model_to_dict(MeetupSpot.objects.get(pk=dict['meetup_spot_id']))
            except Exception as meetup_spot_e:
                pass

        if dict.get('crew'):
            dict['crew_id'] = dict['crew']
            try:
                dict['crew'] = model_to_dict(Crew.objects.get(pk=dict['crew_id']))
            except Exception as crew_e:
                pass
        else:
            crews = Crew.objects.filter(meetup_id=dict.get('id'))
            if len(crews) > 0:
                dict['crew'] = model_to_dict(crews[0])
    return dicts