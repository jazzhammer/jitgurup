import json

import requests

from test_crew_template import erase_default_crew_template

from test_spot_type import erase_default_spot_type
from test_meetup_template import erase_default_meetup_template

from test_org import erase_default_org

from test_facility import erase_default_facility

from test_meetup_spot import erase_default_meetup_spot
from test_person import create_default_person, create_default_person_for_names, erase_default_person
from test_user import create_default_user, erase_default_user, get_default_user, create_default_user_for_names
from test_crew import create_default_crew, create_default_crew_for_name, erase_default_crew
from test_meetup_role import create_default_meetup_role, create_default_meetup_role_for_name_description, erase_default_meetup_role
from test_meetup import create_default_meetup, erase_default_meetup
url_test = 'http://localhost:8000/api/signups'


def test_signup():
    (
        created,
        person,
        crew,
        meetup_role,
        created_by,
        meetup,
        meetup_templatem,
        crew_templatem,
        orgm,
        facilitym,
        meetup_spotm,
        facility2m,
        org2m,
        spot_typem,
        org3m,
        org4m,
        facility3m,
        org5m,
        meetup_spot2m,
        crewm,
        facility4m,
        org6m,
        spot_type2m,
        created_by2,
    ) = create_default_signup()
    (
        updated,
        next_meetup_role,
        next_person,
        next_crew,
    ) = update_default_signup(created)
    delete_default_signup(created.get('id'))
    erase_default_signup(created.get('id'))

    erase_default_user(created_by.get('id'))
    if created_by2:
        erase_default_user(created_by2.get('id'))

    erase_default_person(next_person.get('id'))
    erase_default_person(person.get('id'))

    erase_default_meetup_role(meetup_role.get('id'))
    erase_default_meetup_role(next_meetup_role.get('id'))
    erase_default_meetup_role(meetup_role.get('id'))

    erase_default_meetup(meetup.get('id'))

    erase_default_crew(crew.get('id'))
    erase_default_crew(next_crew.get('id'))
    erase_default_crew(crewm.get('id'))


    erase_default_meetup_template(meetup_templatem.get('id'))

    erase_default_meetup_spot(meetup_spotm.get('id'))
    erase_default_meetup_spot(meetup_spot2m.get('id'))

    erase_default_facility(facilitym.get('id'))
    erase_default_facility(facility2m.get('id'))
    erase_default_facility(facility3m.get('id'))
    erase_default_facility(facility4m.get('id'))

    erase_default_crew_template(crew_templatem.get('id'))

    erase_default_org(orgm.get('id'))
    erase_default_org(org2m.get('id'))
    erase_default_org(org3m.get('id'))
    erase_default_org(org4m.get('id'))
    erase_default_org(org5m.get('id'))
    erase_default_org(org6m.get('id'))

    erase_default_spot_type(spot_typem.get('id'))
    erase_default_spot_type(spot_type2m.get('id'))


def update_default_signup(updatable):
    next_meetup_role = create_default_meetup_role_for_name_description('another name', 'another description')
    next_person = create_default_person_for_names('another last', 'another first')
    next_crew = create_default_crew_for_name('another crew')

    updatable['person_id'] = next_person.get('id')
    updatable['meetup_role_id'] = next_meetup_role.get('id')
    updatable['crew_id'] = next_crew.get('id')
    response = requests.put(url_test, data=updatable)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('meetup_role') == next_meetup_role.get('id')
    assert updated.get('person') == next_person.get('id')
    assert updated.get('crew') == next_crew.get('id')
    assert updated.get('deleted') == False
    return (
        updated,
        next_meetup_role,
        next_person,
        next_crew,
    )

def erase_signups_for_default_user():
    users = get_default_user()
    if users:
        for user in users:
            response = requests.get(url_test, params={
                'created_by_id': user.get('id')
            })
            deletables = json.loads(response.content.decode('utf8'))
            for deletable in deletables:
                erase_signup(deletable.get('id'))

def create_default_signup():
    erase_signups_for_default_user()
    person = create_default_person()
    crew = create_default_crew()
    meetup_role = create_default_meetup_role()
    created_by = create_default_user_for_names('test_signup', 'test_signup_first', 'signup_user')
    (
        meetup,
        meetup_templatem,
        crew_templatem,
        orgm,
        facilitym,
        meetup_spotm,
        facility2m,
        org2m,
        spot_typem,
        org3m,
        org4m,
        facility3m,
        org5m,
        meetup_spot2m,
        crewm,
        facility4m,
        org6m,
        spot_type2m,
        created_by2,
    ) = create_default_meetup()

    response = requests.post(url_test, data={
        'person_id': person.get('id'),
        'meetup_role_id': meetup_role.get('id'),
        'crew_id': crew.get('id'),
        'created_by_id': created_by.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))

    if created:
        assert created.get('person') == person.get('id')
        assert created.get('crew') == crew.get('id')
        assert created.get('meetup_role') == meetup_role.get('id')
        assert not created.get('deleted')

    return (
        created,
        person,
        crew,
        meetup_role,
        created_by,
        meetup,
        meetup_templatem,
        crew_templatem,
        orgm,
        facilitym,
        meetup_spotm,
        facility2m,
        org2m,
        spot_typem,
        org3m,
        org4m,
        facility3m,
        org5m,
        meetup_spot2m,
        crewm,
        facility4m,
        org6m,
        spot_type2m,
        created_by2,
    )

def delete_default_signup(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

def erase_default_signup(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300


def erase_signup(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


