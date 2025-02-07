from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.toolset import Toolset
from api.serializers.toolset_serializer import ToolsetSerializer


# from api.serializers.toolset_serializer import ToolsetSerializer

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def toolsets(request: HttpRequest, *args, **kwargs):
    if request.method == 'PUT':
        id = request.data.get('id')
        if id:
            try:
                id = int(id)
                found = Toolset.objects.get(pk=id)
                user_id = request.data.get('user_id')
                if user_id:
                    dupes = Toolset.objects.filter(user_id=user_id).exclude(id=id)
                    if len(dupes) > 0:
                        return JsonResponse({"message": f"already toolset with {user_id=}"}, status=400, safe=False)
                    else:
                        found.user_id = user_id
                        found.save()
                        return JsonResponse(model_to_dict(found), status=200, safe=False)
                else:
                    return JsonResponse(model_to_dict(found), status=200, safe=False)
            except:
                return JsonResponse({"detail": f"require valid id to update toolset, found {id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require id to update toolset"}, status=400, safe=False)

    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if id:
            try:
                found = Toolset.objects.get(pk=id)
                if erase:
                    found.delete()
                    return JsonResponse({"message": f"deleted"}, status=200, safe=False)
                else:
                    found.deleted = True
                    found.save()
                    return JsonResponse(model_to_dict(found), status=200, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"no toolset for {id=}"}, status=404, safe=False)
        else:
            return JsonResponse({"detail": f"require id to delete toolset"}, status=400, safe=False)

    if request.method == 'POST':
        user_id = request.data.get('user_id')
        if user_id:
            if len(user_id.strip()) > 0:
                user = User.objects.filter(pk=user_id)
                if user:
                    created = Toolset.objects.create(user=user)
                    return JsonResponse(model_to_dict(created, fields=[field.name for field in created._meta.fields]), status=201, safe=False)
            else:
                return JsonResponse({"detail": f"require non blank user_id for toolset, found {user_id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require user for toolset, found {user_id=}"}, status=400, safe=False)

    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        id = request.GET.get('id')
        if id:
            try:
                id = int(id)
                found = Toolset.objects.get(pk=id, deleted=False)
                if found:
                    return JsonResponse(model_to_dict(found), status=200, safe=False)
                else:
                    return JsonResponse({"message": f"not found for {id=}"}, status=404, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"error retrieving toolset for {id=}"}, status=400, safe=False)
        if user_id:
            if len(user_id.strip()) > 0:
                founds = Toolset.objects.filter(user_id=user_id, deleted=False)
                if founds:
                    return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)
                else:
                    return JsonResponse([], status=200, safe=False)
            else:
                return JsonResponse({"message": f"error retrieving toolset for {user_id=}"}, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "require name or facility_id for toolset query"
            }, status=400)