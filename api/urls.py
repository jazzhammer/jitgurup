from django.urls import path

from .views import user_view, user_preferences_view, orgs_view, security_permissions_view

urlpatterns = [
    path('', user_view.api_home),
    path('orgs/<int:org_id>', orgs_view.org),
    path('orgs', orgs_view.orgs),
    path('persons', user_view.persons),
    path('users', user_view.users),
    path('users/<int:user_id>', user_view.user),
    path('users/permission', security_permissions_view.security_permissions),
    path('users/preference', user_preferences_view.preferences),
    path('users/orgs', orgs_view.user_orgs),
    path('tests/reset', user_view.reset_tests),
    path('tests/reset/org', orgs_view.reset_tests),
    path('tests/reset/security', user_view.reset_tests_security),
    path('tests/reset/users/preference', user_preferences_view.reset_tests),
    path("seed/default_users", user_view.seed_default_users),
    path("seed/default_orgs", user_view.seed_default_orgs),
    path("seed/default_user_orgs", user_view.seed_default_user_orgs),
]
