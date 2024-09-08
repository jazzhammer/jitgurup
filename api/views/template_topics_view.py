from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models.meetup_template import MeetupTemplate
from api.models.template_topic import TemplateTopic
from api.models.topic import Topic

@api_view(['GET'])
def template_topic(request, template_topic_id):
    found = TemplateTopic.objects.get(pk=template_topic_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST'])
def reset_tests(request):
    TemplateTopic.objects.all().delete()
    return JsonResponse({
        "message": "success"
    }, status=200)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def template_topics(request, *args, **kwargs):
    if request.method == 'DELETE':
        id: int = request.GET.get('id')
        try:
            found = TemplateTopic.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"template_topic not found for update {id=}",
            }, status=404, safe=False)
        found.deleted = True
        found.save()
        return JsonResponse({
            "message": "success",
            "deleted": model_to_dict(found)
        }, status=200, safe=False)

    if request.method == 'PUT':
        id: int = request.data.get('id')
        topic_id: int = request.data.get('topic_id')
        meetup_template_id: int = request.data.get('meetup_template_id')
        try:
            found = TemplateTopic.objects.get(pk=id)
        except:
            return JsonResponse({
                "error": f"template_topic not found for update {id=}",
            }, status=404, safe=False)

        dupes: QuerySet = TemplateTopic.objects.all()
        dupes.exclude(id=id)

        if topic_id:
            try:
                topic = Topic.objects.get(pk=topic_id)
            except:
                return JsonResponse({
                    "error": f"require valid topic_id to update template_topic, found {topic_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(topic_id=topic_id)
        if meetup_template_id:
            try:
                meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
            except:
                return JsonResponse({
                    "error": f"require valid meetup_template_id to update template_topic, found {meetup_template_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(meetup_template_id=meetup_template_id)

        if dupes and dupes.count() > 0:
            return JsonResponse({
                "error": f"already template_topic for {topic_id=}, {meetup_template_id=}",
            }, status=400, safe=False)

        found.topic = topic
        found.meetup_template = meetup_template
        found.deleted = False
        found.save()
        return JsonResponse({
            "message": "success",
            "updated": model_to_dict(found)
        }, status=200, safe=False)

    if request.method == 'POST':

        topic_id: str = request.data.get('topic_id')
        meetup_template_id: str = request.data.get('meetup_template_id')
        dupes: QuerySet = TemplateTopic.objects.all()

        if topic_id:
            try:
                topic = Topic.objects.get(pk=topic_id)
            except:
                return JsonResponse({
                    "error": f"require valid topic_id to update template_topic, found {topic_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(topic_id=topic_id)
        if meetup_template_id:
            try:
                meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
            except:
                return JsonResponse({
                    "error": f"require valid meetup_template_id for template_topic, found {meetup_template_id=}",
                }, status=400, safe=False)
            dupes = dupes.filter(meetup_template_id=meetup_template_id)
        else:
            return JsonResponse({
                "error": f"template_topic requires topic, found {topic_id=}",
            }, status=400, safe=False)

        if dupes and dupes.count() > 0:
            for dupe in dupes:
                if dupe.deleted:
                    dupe.deleted = False
                    dupe.save()
                    return JsonResponse({
                        "message": "success",
                        "created": model_to_dict(dupe)
                    }, status=201, safe=False)
        created = TemplateTopic.objects.create(
            topic=topic,
            meetup_template=meetup_template
        )

        return JsonResponse({
            "message": "success",
            "created": model_to_dict(created)
        }, status=201, safe=False)

    if request.method == 'GET':
        topic_id = request.GET.get('topic_id')
        meetup_template_id = request.GET.get("meetup_template_id")
        founds = TemplateTopic.objects.all()
        filtered = False
        if topic_id:
            filtered = True
            founds = founds.filter(topic_id=topic_id)
        if meetup_template_id:
            filtered = True
            founds = founds.filter(meetup_template_id=meetup_template_id)
        if not filtered:
            founds = TemplateTopic.objects.all()[:10]
        if founds:
            return JsonResponse({
                "message": "success",
                "matched": [model_to_dict(instance) for instance in founds]
            }, status=200)
