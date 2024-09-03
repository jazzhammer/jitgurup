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
    required_by_id = request.GET.get('required_by_id')
    rule_numerator = request.GET.get('rule_numerator')
    deleted = request.GET.get('deleted')
    if not deleted:
        deleted = False
    founds = PrereqSet.objects.filter(deleted=deleted)
    if required_by_id:
        required_by_template = MeetupTemplate.objects.get(pk=required_by_id)
        founds = founds.filter(required_by=required_by_template)
    else:
        return JsonResponse({
            "error": f"require required_by meetup template id for search, found {required_by_id=}"
        }, status=400, safe=False)
    if rule_numerator:
        founds = founds.filter(required_by=required_by_template)
    return JsonResponse({
        "message": f"success",
        "matched": [model_to_dict(instance) for instance in founds]
    }, status=200, safe=False)
def post_prereq_sets(request: HttpRequest):
    required_by_id = request.data.get('required_by_id')
    if required_by_id:
        required_by_template = MeetupTemplate.objects.get(pk=required_by_id)
        created = PrereqSet.objects.create(required_by=required_by_template)
    else:
        return JsonResponse({
            "error": f"require required_by meetup template id to create, {required_by_id=}"
        }, status=400, safe=False)
    return JsonResponse({
        "message": f"success",
        "created": model_to_dict(created)
    }, status=200, safe=False)
def delete_prereq_sets(request: HttpRequest):
    id = request.GET.get('id')
    found: QuerySet = PrereqSet.objects.get(pk=id)
    if not found:
        return JsonResponse({
            "error": f"not found for {id=}"
        }, status=404, safe=False)
    else:
        found.deleted = True
        found.save()
        return JsonResponse({
            "message": f"success",
            "deleted": model_to_dict(found)
        }, status=200, safe=False)
def put_prereq_sets(request: HttpRequest):
    id = request.data.get('id')
    found = PrereqSet.objects.get(pk=id)
    rule_numerator = request.data.get('rule_numerator')
    if not found:
        return JsonResponse({
            "error": f"not found for {id=}"
        }, status=404, safe=False)
    required_by_id = request.data.get('required_by_id')
    if required_by_id:
        required_by = MeetupTemplate.objects.get(pk=required_by_id)
        if not required_by:
            return JsonResponse({
                "error": f"require required_by meetup template id to update, found {required_by_id=}"
            }, status=400, safe=False)
        else:
            found.required_by = required_by
    if rule_numerator:
        found.rule_numerator = rule_numerator
    found.save()
    return JsonResponse({
        "message": f"success",
        "updated": model_to_dict(found)
    }, status=200, safe=False)
