from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.meetup_role import MeetupRole
from api.serializers.meetup_role_serializer import MeetupRoleSerializer


@api_view(["POST", "GET", "PUT", "DELETE"])
def meetup_roles(request: HttpRequest, **kwargs):

    if request.method == 'POST':
        data = request.data
        created = MeetupRole.objects.create(name=data.get('name'))
        return JsonResponse(model_to_dict(created), status=200, safe=False)

    elif request.method == 'GET':
        id = request.GET.get('id')
        found = MeetupRole.objects.get(pk=id)
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)

    elif request.method == 'PUT':
        id = request.data.get('id')
        name = request.data.get('name')
        found = MeetupRole.objects.get(pk=id)
        if name:
            found.name = name
        found.save()
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)

    elif request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        found = MeetupRole.objects.get(pk=id)
        if erase:
            found.delete()
        else:
            found.deleted = True
            found.save()
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)

