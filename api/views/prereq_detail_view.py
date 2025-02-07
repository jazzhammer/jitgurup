from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from api.models.meetup_template import MeetupTemplate
from api.models.prereq_detail import PrereqDetail
from api.models.prereq_set import PrereqSet


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def prereq_details(request: HttpRequest):
    if request.method == 'GET':
        return get_prereq_details(request)
    if request.method == 'POST':
        return post_prereq_details(request)
    if request.method == 'DELETE':
        return delete_prereq_details(request)
    if request.method == 'PUT':
        return put_prereq_details(request)

def get_prereq_details(request: HttpRequest):
    meetup_template_id = request.GET.get('meetup_template_id')
    prereq_set_id = request.GET.get('prereq_set_id')
    mandatory = request.GET.get('mandatory')
    deleted = request.GET.get('deleted')

    if deleted is None:
        deleted = False
    founds = PrereqDetail.objects.filter(deleted=deleted)
    filtered = False
    if meetup_template_id:
        filtered = True
        meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
        founds = founds.filter(template=meetup_template)
    if prereq_set_id:
        filtered = True
        prereq_set = PrereqSet.objects.get(pk=prereq_set_id)
        founds = founds.filter(prereq_set=prereq_set)
    if mandatory is not None:
        filtered = True
        founds = founds.filter(mandatory=mandatory)
    if not filtered:
        founds = founds[:10]
    return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)

def post_prereq_details(request: HttpRequest):

    prereq_set_id = request.data.get('prereq_set_id')
    try:
        prereq_set = PrereqSet.objects.get(pk=prereq_set_id)
    except:
        return JsonResponse({
            "error": f"require prereq_set id to create, {prereq_set_id=}"
        }, status=400, safe=False)

    meetup_template_id = request.data.get('meetup_template_id')
    try:
        meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
    except:
        return JsonResponse({
            "error": f"require meetup_template id to create, {meetup_template_id=}"
        }, status=400, safe=False)


    created = PrereqDetail.objects.create(meetup_template=meetup_template, prereq_set=prereq_set)
    return JsonResponse(model_to_dict(created), status=201, safe=False)

def delete_prereq_details(request: HttpRequest):
    id = request.GET.get('id')
    erase = request.GET.get('erase')
    found: QuerySet = PrereqDetail.objects.get(pk=id)
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

def put_prereq_details(request: HttpRequest):
    id = request.data.get('id')
    found = PrereqDetail.objects.get(pk=id)

    if not found:
        return JsonResponse({
            "error": f"not found for {id=}"
        }, status=404, safe=False)

    meetup_template_id = request.data.get('meetup_template_id')
    if meetup_template_id:
        try:
            meetup_template = MeetupTemplate.objects.get(pk=meetup_template_id)
            found.meetup_template = meetup_template
        except:
            pass

    prereq_set_id = request.data.get('prereq_set_id')
    if prereq_set_id:
        try:
            prereq_set = PrereqSet.objects.get(pk=prereq_set_id)
            found.prereq_set = prereq_set
        except:
            pass

    mandatory = request.data.get('mandatory')
    if mandatory is not None:
        found.mandatory = mandatory

    found.save()
    return JsonResponse(model_to_dict(found), status=200, safe=False)
