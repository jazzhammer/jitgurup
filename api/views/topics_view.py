from django.forms import model_to_dict
from rest_framework.decorators import api_view

from api.models.subject import Subject
from api.models.topic import Topic
from django.http import JsonResponse, HttpRequest


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def topics(request: HttpRequest):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if not id:
            return JsonResponse({
                "error": f"require id to delete topic, found {id=}"
            }, status=400, safe=False)
        else:
            found = Topic.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"topic not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'PUT':
        id = request.data.get('id')
        subject_id =request.data.get('subject_id')
        if not id:
            return JsonResponse({
                "error": f"require id to update topic, found {id=}"
            }, status=400, safe=False)
        else:
            found = Topic.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"topic not found for {id=}"
                }, status=404, safe=False)

            name: str = request.data.get("name")
            if name:
                if len(name.strip()) > 0:
                    found.name = name.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank name to update topic, found {name=}"
                    }, status=400, safe=False)
            if subject_id:
                found.subject = Subject.objects.get(pk=subject_id)
                found.save()
            return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        name: str = request.data.get('name')
        subject_id: str = request.data.get('subject_id')
        if name:
            if len(name.strip()) > 0 and subject_id:
                already = Topic.objects.filter(name__iexact=name, subject_id=subject_id).first()
                if already is None:
                    created = Topic.objects.create(name=name.strip(), subject_id=subject_id)
                    return JsonResponse(model_to_dict(created, fields=[field.name for field in created._meta.fields]), status=201, safe=False)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse(model_to_dict(already, fields=[field.name for field in already._meta.fields]), status=200, safe=False)
            else:
                return JsonResponse({
                    "error": f"require non blank name and subject_id for new topic, found {name=} {subject_id=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "error": f"require non blank name and subject_id for new topic, found {name=} {subject_id=}"
            }, status=400, safe=False)

    elif request.method == 'GET':
        name = request.GET.get('name')
        subject_id = request.GET.get('subject_id')
        founds = Topic.objects.all()
        if name:
            founds = founds.filter(name__icontains=name, deleted=False)
        if subject_id:
            founds = founds.filter(subject_id=subject_id, deleted=False)
        if founds:
            dicts = [model_to_dict(instance) for instance in founds]
            for dict in dicts:
                subject_id = dict.get('subject')
                try:
                    subject = Subject.objects.get(pk=subject_id)
                    dict['subject'] = model_to_dict(subject)
                except Exception as subject_e:
                    pass
            return JsonResponse(dicts, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)


