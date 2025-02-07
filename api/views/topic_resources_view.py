import io

from django.forms import model_to_dict
from rest_framework.decorators import api_view

from api.models.topic import Topic
from api.models.topic_resource import TopicResource
from django.http import JsonResponse, HttpRequest


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def topic_resources(request: HttpRequest, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to delete topic_resource, found {id=}"
            }, status=400, safe=False)
        else:
            found = TopicResource.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"topic_resource not found for {id=}"
                }, status=404, safe=False)
            else:
                found.deleted = True
                found.save()
                return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'PUT':
        id = request.data.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to update topic_resource, found {id=}"
            }, status=400, safe=False)
        else:
            found = TopicResource.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"topic_resource not found for {id=}"
                }, status=404, safe=False)

            description: str = request.data.get("description")
            if description:
                if len(description.strip()) > 0:
                    found.description = description.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank description to update topic_resource, found {description=}"
                    }, status=400, safe=False)
            return JsonResponse(model_to_dict(found), status=200)

    if request.method == 'POST':
        description: str = request.data.get('description')
        topic_id: int = request.data.get('topic_id')
        url: str = request.data.get('url')
        if description:
            if len(description.strip()) == 0:
                return JsonResponse({
                    "error": f"require non blank description for new topic_resource, found {description=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "message": f"topic_resource requires description. found {description=}"
            }, status=400)
        if topic_id:
            topic = Topic.objects.get(pk=topic_id)
        if not url:
            return JsonResponse({
                "message": f"topic_resource requires url. found {url=}"
            }, status=400)
        created = TopicResource.objects.create(topic=topic, url=url, description=description)
        return JsonResponse(model_to_dict(created), status=201, safe=False)

    elif request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = TopicResource.objects.get(pk=id)
                return JsonResponse([model_to_dict(found)],
                status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no topic_resource found for {id=}'
                }, status=404, safe=False)

        description = request.GET.get('description')
        topic_id = request.GET.get('topic_id')
        filtered = False
        founds = TopicResource.objects.filter(deleted=False)
        if description:
            filtered = True
            founds = founds.filter(description__icontains=description)
        if topic_id:
            filtered = True
            founds = founds.filter(topic_id=topic_id)
        if filtered:
            if founds is not None:
                return JsonResponse([model_to_dict(instance) for instance in founds], status=200)
            else:
                return JsonResponse({
                    "message": f"no topic_resource found {description=}, {topic_id=}"
                }, status=404)
        else:
            founds = TopicResource.objects.all()[:10]
            return JsonResponse([model_to_dict(instance) for instance in founds], status=200)


