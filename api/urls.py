from django.contrib import admin
from django.urls import path

from . import user_views
from . import security_permissions_view
from . import orgs_view

urlpatterns = [
    path('', user_views.api_home),
    path('persons', user_views.persons),
    path('users', user_views.users),
    path('users/permission', security_permissions_view.security_permissions),
    path('users/orgs', orgs_view.user_orgs),
    path('tests/reset', user_views.reset_tests),
    path('tests/reset/security', user_views.reset_tests_security)
]
