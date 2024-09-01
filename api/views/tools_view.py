from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models.tool import Tool
from api.serializers.tool_serializer import ToolSerializer


# from api.serializers.tool_serializer import ToolSerializer


@api_view(['GET'])
def tool(request, tool_id):
    found = Tool.objects.get(id=tool_id)
    if found is not None:
        return JsonResponse(model_to_dict(found, fields=[field.name for field in found._meta.fields]), status=200)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=404)

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def tools(request: HttpRequest, *args, **kwargs):
    if request.method == 'PUT':
        id = request.data.get('id')
        if id:
            try:
                id = int(id)
                found = Tool.objects.get(pk=id)
                name = request.data.get('name')
                if name:
                    if len(name.strip()) > 0:
                        found.name = name
                    else:
                        return JsonResponse({"detail": f"require non blank name if updating tool.name, found {name=}"},
                                            status=400,
                                            safe=False
                        )
                found.save()
                return JsonResponse({'message': 'updated', 'updated': model_to_dict(found)}, status=200, safe=False)
            except:
                return JsonResponse({"detail": f"require valid id to update tool, found {id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require id to update tool"}, status=400, safe=False)
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if id:
            try:
                found = Tool.objects.get(pk=id)
                found.deleted = True
                found.save()
                return JsonResponse({
                    "message": f"deleted for key {id=}",
                    "deleted": model_to_dict(found)
                }, status=200, safe=False)
            except Exception as e:
                return JsonResponse({"detail": "error", "error": e}, status=500, safe=False)
        else:
            return JsonResponse({"detail": f"require id to delete tool"}, status=400, safe=False)
    if request.method == 'POST':
        name = request.data.get('name')
        if name:
            if len(name.strip()) > 0:
                already = Tool.objects.filter(name=name).first()
                if not already:
                    created = Tool.objects.create(name=name)
                    return JsonResponse({
                        "message": "success",
                        "created": model_to_dict(created, fields=[field.name for field in created._meta.fields])
                    }, status=201)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse({
                        "message": "previously created",
                        "created": model_to_dict(already, fields=[field.name for field in already._meta.fields])
                    }, status=200)
            else:
                return JsonResponse({"detail": f"require non blank name for tool, found {name=}"}, status=400, safe=False)
        else:
            return JsonResponse({"detail": f"require name for tool, found {name=}"}, status=400, safe=False)
    if request.method == 'GET':
        name = request.GET.get('name')
        id = request.GET.get('id')
        if id:
            try:
                id = int(id)
                found = Tool.objects.get(pk=id, deleted=False)
                if found:
                    return JsonResponse(model_to_dict(found), status=200, safe=False)
                else:
                    return JsonResponse({"message": f"not found for {id=}"}, status=404, safe=False)
            except Exception as e:
                return JsonResponse({"message": f"error retrieving tool for {id=}"}, status=400, safe=False)
        if name:
            if len(name.strip()) > 0:
                founds = Tool.objects.filter(name__contains=name.strip(), deleted=False)
                if founds:
                    return JsonResponse({
                        "message": "success",
                        "matched": [model_to_dict(instance) for instance in founds]
                    }, status=200, safe=False)
                else:
                    return JsonResponse([], status=200, safe=False)
            else:
                return JsonResponse({"message": f"error retrieving tool for {name=}"}, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "require name or facility_id for tool query"
            }, status=400)