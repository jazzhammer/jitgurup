from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_home),
    path('persons', views.persons),
    path('users', views.users),
    path('tests/reset', views.reset_tests),
    path('tests/reset/security', views.reset_tests_security)
]
