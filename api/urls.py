from django.urls import path

from .views import user_view, user_preferences_view, orgs_view, security_permissions_view, facilitys_view, \
    meetup_spots_view, spot_types_view

urlpatterns = [
    path('', user_view.api_home),
    path('facilitys', facilitys_view.facilitys),
    path('facility/<int:facility_id>', facilitys_view.facility),
    path('meetup_spots', meetup_spots_view.meetup_spots),
    path('meetup_spot/<int:meetup_spot_id>', meetup_spots_view.meetup_spot),
    path('orgs', orgs_view.orgs),
    path('orgs/<int:org_id>', orgs_view.org),
    path('persons', user_view.persons),
    path('spot_types', spot_types_view.spot_types),
    path('spot_type/<int:spot_type_id>', spot_types_view.spot_type),
    path('users', user_view.users),
    path('users/<int:user_id>', user_view.user),
    path('users/permission', security_permissions_view.security_permissions),
    path('users/preference', user_preferences_view.preferences),
    path('users/orgs', orgs_view.user_orgs),
    path('tests/reset', user_view.reset_tests),
    path('tests/reset/facility', facilitys_view.reset_tests),

    path('tests/reset/org', orgs_view.reset_tests),
    path('tests/reset/security', user_view.reset_tests_security),
    path('tests/reset/users/preference', user_preferences_view.reset_tests),
    path("seed/default_users", user_view.seed_default_users),
    path("seed/default_orgs", user_view.seed_default_orgs),
    path("seed/default_user_orgs", user_view.seed_default_user_orgs),
]
