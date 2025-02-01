import json

import requests

from test_facility import create_default_facility, create_default_facility_for_name_description

url_test = 'http://localhost:8000/api/meetup_roles'

TEST_MEETUP_ROLE_NAME = "thebestmeetup_role"
TEST_MEETUP_ROLE_NEXT_NAME = "thenextbestmeetup_role"
TEST_MEETUP_ROLE_DESCRIPTION = "thebestmeetup_role_description"
TEST_MEETUP_ROLE_NEXT_DESCRIPTION = "thenextbestmeetup_role_description"


def test_meetup_role():
    created = create_default_meetup_role()
    updated = update_default_meetup_role(created)
    delete_default_meetup_role(updated.get('id'))
    erase_default_meetup_role(updated.get('id'))

def update_default_meetup_role(updatable):

    updatable['name'] = TEST_MEETUP_ROLE_NEXT_NAME


    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_MEETUP_ROLE_NEXT_NAME
    assert updated.get('deleted') == False
    return updated

def create_default_meetup_role():
    return create_default_meetup_role_for_name_description(TEST_MEETUP_ROLE_NAME, TEST_MEETUP_ROLE_DESCRIPTION)

def create_default_meetup_role_for_name_description(name: str, description: str):
    response = requests.post(url_test, data={
        'name': name,
        'description': description,
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('name') == name
    assert not created.get('deleted')
    return created


def erase_default_meetup_role(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300

def delete_default_meetup_role(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')
