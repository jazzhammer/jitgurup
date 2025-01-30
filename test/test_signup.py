import json

import requests

from test_person import create_default_person, create_default_person_for_names, erase_default_person
from test_user import create_default_user, erase_default_user, get_default_user
from test_crew import create_default_crew, create_crew_for_name
from test_meetup_role import create_default_meetup_role, create_default_meetup_role_for_name_description
from test_meetup import create_default_meetup, erase_default_meetup
url_test = 'http://localhost:8000/api/signups'


def test_signup():
    created = create_default_signup()

    updated = update_default_signup(created)
    delete_default_signup(created.get('id'))
    erase_default_signup(created.get('id'))
    erase_default_user()
    erase_default_person()

def update_default_signup(updatable):
    next_meetup_role = create_default_meetup_role_for_name_description('another name', 'another description')
    next_person = create_default_person_for_names('another last', 'another first')
    next_crew = create_crew_for_name('another crew')

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
    erase_default_person()
    erase_signups_for_default_user()
    erase_default_user()
    person = create_default_person()
    crew = create_default_crew()
    meetup_role = create_default_meetup_role()
    created_by = create_default_user()
    meetup = create_default_meetup()
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
    return created

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


