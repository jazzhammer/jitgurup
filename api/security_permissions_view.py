from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse

@api_view(["GET"])
def security_permissions(request, *args, **kwargs):
    print(f"security_permissions({args})")
    user_id = int(request.query_params['user_id'])
    permission = request.query_params['permission']
    user = User.objects.get(id=user_id)
    return JsonResponse({
        "hasPermission": user.has_perm(permission)
    }, status=200)
