from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from api.models.meetup_template import MeetupTemplate
from api.models.prereq_set import PrereqSet


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def prereq_sets(request: HttpRequest):
    if request.method == 'GET':
        return get_prereq_sets(request)
    if request.method == 'POST':
        return post_prereq_sets(request)
    if request.method == 'DELETE':
        return delete_prereq_sets(request)
    if request.method == 'PUT':
        return put_prereq_sets(request)

def get_prereq_sets(request: HttpRequest):
    meetup_template_id = request.GET.get('meetup_template_id')
    rule_numerator = request.GET.get('rule_numerator')
    deleted = request.GET.get('deleted')
    if not deleted:
        deleted = False
    founds = PrereqSet.objects.filter(deleted=deleted)
    if meetup_template_id:
        meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
        founds = founds.filter(meetup_template=meetup_template)
    else:
        return JsonResponse({
            "error": f"require meetup_template meetup template id for search, found {meetup_template_id=}"
        }, status=400, safe=False)
    if rule_numerator:
        founds = founds.filter(meetup_template=meetup_template)
    return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)

def post_prereq_sets(request: HttpRequest):
    meetup_template_id = request.data.get('meetup_template_id')
    if meetup_template_id:
        meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
        created = PrereqSet.objects.create(meetup_template=meetup_template)
    else:
        return JsonResponse({
            "error": f"require meetup_template meetup template id to create, {meetup_template_id=}"
        }, status=400, safe=False)
    return JsonResponse(model_to_dict(created), status=200, safe=False)

def delete_prereq_sets(request: HttpRequest):
    id = request.GET.get('id')
    erase = request.GET.get('erase')
    found: QuerySet = PrereqSet.objects.get(pk=id)
    if not found:
        return JsonResponse({
            "error": f"not found for {id=}"
        }, status=404, safe=False)
    else:
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

def put_prereq_sets(request: HttpRequest):
    id = request.data.get('id')
    found = PrereqSet.objects.get(pk=id)
    rule_numerator = request.data.get('rule_numerator')
    if not found:
        return JsonResponse({
            "error": f"not found for {id=}"
        }, status=404, safe=False)
    meetup_template_id = request.data.get('meetup_template_id')
    if meetup_template_id:
        meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
        if not meetup_template:
            return JsonResponse({
                "error": f"require meetup_template meetup template id to update, found {meetup_template_id=}"
            }, status=400, safe=False)
        else:
            found.meetup_template = meetup_template
    if rule_numerator:
        found.rule_numerator = rule_numerator
    found.save()
    return JsonResponse(model_to_dict(found), status=200, safe=False)
