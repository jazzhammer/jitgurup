from django.contrib import admin
from django.urls import path

from . import views
from . import security_permissions_view

urlpatterns = [
    path('', views.api_home),
    path('persons', views.persons),
    path('users', views.users),
    path('users/permission', security_permissions_view.security_permissions),
    path('tests/reset', views.reset_tests),
    path('tests/reset/security', views.reset_tests_security)
]
