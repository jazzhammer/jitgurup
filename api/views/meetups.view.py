from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.meetup import Meetup
from api.models.meetup_template import MeetupTemplate
from api.serializers.meetup_serializer import MeetupSerializer


@api_view(["POST", "GET", "PUT", "DELETE"])
def meetups(request, meetup_id, **kwargs):
    if request.method == 'POST':
        start_at: str = request.data.get('start_at')
        try:
            start_at_dt = parse_datetime(start_at)
        except:
            return JsonResponse({
                'error': f"require valid start_at for meetup, found {start_at=}"
            }, status=400, safe=False)

        # in minutes
        duration: int = request.data.get('duration')
        meetup_template_id: int = request.data.get('meetup_template_id')
        try:
            meetup_template: MeetupTemplate = MeetupTemplate.objects.get(pk=meetup_template_id)
        except:
            return JsonResponse({
                'error': f"require valid meetup_template_id for meetup, found {meetup_template_id=}"
            }, status=400, safe=False)

        name: str = request.data.get('name')
        if not name or len(name.strip()) == 0:
            name = meetup_template.name
        created = Meetup.objects.create(
            start_at=start_at_dt,
            duration=duration,
            meetup_template=meetup_template,
            name=name
        )
        return JsonResponse({
            "message": "success",
            "created": model_to_dict(created)
        }, status=201, safe=False)

    if request.method == 'GET':
        id = request.data.get('id')
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


        if meetup_id is not None:
            found = Meetup.objects.get(id=meetup_id)
            return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
