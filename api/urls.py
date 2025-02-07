from django.urls import path

from .views import user_view, user_preferences_view, orgs_view, security_permissions_view, facilitys_view, \
    meetup_spots_view, spot_types_view, user_persons_view, user_meetup_spots_view, persons_view, org_persons_view, \
    meetup_templates_view, tools_view, focuss_view, subjects_view, topics_view, prereq_set_view, prereq_detail_view, \
    roles_view, crew_templates_view, template_roles_view, crews_view, signups_view, template_topics_view, \
    topic_resources_view, meetup_roles_view, meetup_view, village_view, learning_modalitys_view, \
    preferred_modalitys_view, user_session_view

urlpatterns = [
    path('crews', crews_view.crews),
    path('crew_templates', crew_templates_view.crew_templates),
    path('facilitys', facilitys_view.facilitys),
    path('focuss', focuss_view.focuss),
    path('facility/<int:facility_id>', facilitys_view.facility),
    path('learning_modalitys', learning_modalitys_view.learning_modalitys),
    path('meetup_roles', meetup_roles_view.meetup_roles),
    path('meetup_spots', meetup_spots_view.meetup_spots),
    path('meetup_spot/<int:meetup_spot_id>', meetup_spots_view.meetup_spot),
    path('meetup_templates', meetup_templates_view.meetup_templates),
    path('meetups', meetup_view.meetup),
    path('orgs', orgs_view.orgs),
    path('orgs/<int:org_id>', orgs_view.org),
    path('orgs/person', org_persons_view.org_persons),
    path('orgs/person/<int:org_id>', org_persons_view.org_persons),
    path('persons', persons_view.persons),
    path('persons/<int:person_id>', persons_view.persons),
    path('preferred_modalitys', preferred_modalitys_view.preferred_modalitys),
    path('prereq_details', prereq_detail_view.prereq_details),
    path('prereq_sets', prereq_set_view.prereq_sets),
    path('roles', roles_view.roles),
    path('signups', signups_view.signups),
    path('spot_types', spot_types_view.spot_types),
    path('spot_type/<int:spot_type_id>', spot_types_view.spot_type),
    path('subjects', subjects_view.subjects),
    path('template_roles', template_roles_view.template_roles),
    path('template_topics', template_topics_view.template_topics),
    path('tools', tools_view.tools),
    path('topics', topics_view.topics),
    path('topic_resources', topic_resources_view.topic_resources),
    path('users', user_view.users),
    path('users/<int:user_id>', user_view.user),
    path('users/meetup_spot', user_meetup_spots_view.user_meetup_spots),
    path('users/permission', security_permissions_view.security_permissions),
    path('users/persons', user_persons_view.user_persons),
    path('users/preference', user_preferences_view.preferences),
    path('users/orgs', orgs_view.user_orgs),
    path('users/persons', user_persons_view.user_persons),
    path('users/user_groups', user_view.user_user_groups),
    path('users/usersessions', user_session_view.user_sessions),
    path('tests/reset', user_view.reset_tests),
    path('tests/reset/facility', facilitys_view.reset_tests),

    path('tests/reset/org', orgs_view.reset_tests),
    path('tests/reset/security', user_view.reset_tests_security),
    # path('tests/reset/users/preference', user_preferences_view.reset_tests),
    path("seed/default_users", user_view.seed_default_users),
    path("seed/default_orgs", user_view.seed_default_orgs),
    path("seed/default_user_orgs", user_view.seed_default_user_orgs),
    path("villages", village_view.villages)
]
