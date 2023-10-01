import json

from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(["GET"])
def security_permissions(request, *args, **kwargs):
    params = request.query_params
    if 'user_id' in params:
        user_id = int(request.query_params['user_id'])
        user = User.objects.get(id=user_id)
        permissions = user.get_all_permissions()
        return JsonResponse(json.dumps(permissions, default=list), status=200, safe=False)
    else:
        return JsonResponse({
            "message": "failure"
        }, status=400)
