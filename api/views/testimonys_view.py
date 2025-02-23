from django.forms import model_to_dict
from rest_framework.decorators import api_view

from api.models.testimony import Testimony
from django.http import JsonResponse, HttpRequest


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def testimonys(request: HttpRequest, *args, **kwargs):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        erase = request.GET.get('erase')
        if not id:
            return JsonResponse({
                "error": f"require id to delete testimony, found {id=}"
            }, status=400, safe=False)
        else:
            found = Testimony.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"testimony not found for {id=}"
                }, status=404, safe=False)
            else:
                if erase:
                    found.delete()
                else:
                    found.deleted = True
                    found.save()
                return JsonResponse(model_to_dict(found), status=200)

    if request.method == 'PUT':
        id = request.data.get('id')
        if not id:
            return JsonResponse({
                "error": f"require id to update testimony, found {id=}"
            }, status=400, safe=False)
        else:
            found = Testimony.objects.get(pk=id)
            if not found:
                return JsonResponse({
                    "error": f"testimony not found for {id=}"
                }, status=404, safe=False)

            content: str = request.data.get("content")
            if content:
                if len(content.strip()) > 0:
                    found.content = content.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank content to update testimony, found {content=}"
                    }, status=400, safe=False)
            type: str = request.data.get("type")
            if type:
                if len(type.strip()) > 0:
                    found.type = type.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank type to update testimony, found {type=}"
                    }, status=400, safe=False)

            url: str = request.data.get("url")
            if url:
                if len(url.strip()) > 0:
                    found.url = url.strip()
                    found.save()
                else:
                    return JsonResponse({
                        "error": f"require non blank url to update testimony, found {url=}"
                    }, status=400, safe=False)

            return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'POST':
        content: str = request.data.get('content')
        type: str = request.data.get('type')
        url: str = request.data.get('url')

        if content:
            if len(content.strip()) > 0:
                already = Testimony.objects.filter(content__iexact=content).first()
                if already is None:
                    created = Testimony.objects.create(content=content.strip(), type=type, url=url)
                    return JsonResponse(model_to_dict(created), status=201, safe=False)
                else:
                    already.deleted = False
                    already.save()
                    return JsonResponse(model_to_dict(already), status=200)
            else:
                return JsonResponse({
                    "error": f"require non blank content for new testimony, found {content=}"
                }, status=400, safe=False)
        else:
            return JsonResponse({
                "message": "unable to create for missing minimum fields"
            }, status=400, safe=False)

    elif request.method == 'GET':
        id = request.GET.get('id')

        if id:
            try:
                found = Testimony.objects.get(pk=id)
                return JsonResponse([model_to_dict(found)], status=200, safe=False)
            except:
                return JsonResponse({
                    'error:': f'no testimony found for {id=}'
                }, status=404, safe=False)

        content = request.GET.get('content')
        type = request.GET.get('type')
        url = request.GET.get('url')
        filtered = False
        founds = Testimony.objects.all()
        if content:
            filtered = True
            founds = founds.filter(content__icontains=content, deleted=False)
        if type:
            filtered = True
            founds = founds.filter(type__icontains=type, deleted=False)
        if url:
            filtered = True
            founds = founds.filter(url__icontains=url, deleted=False)

        if not filtered:
            founds = Testimony.objects.all()[:10]

        return JsonResponse([model_to_dict(instance) for instance in founds], status=200, safe=False)


