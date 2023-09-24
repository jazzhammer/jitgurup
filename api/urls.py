from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_home),
    path('persons', views.persons),
    path('tests/reset', views.reset_tests)
]
