import datetime
import json
import time

import requests

from test_meetup_template import create_default_meetup_template
from test_org import create_default_org
from test_facility import create_default_facility
from test_meetup_spot import create_default_meetup_spot
from test_crew import create_default_crew


url_test = 'http://localhost:8000/api/meetups'

TEST_MEETUP_NAME = "thebestmeetup"
TEST_MEETUP_NEXT_NAME = "thenextbestmeetup"
TEST_MEETUP_DESCRIPTION = "thebestmeetup_description"
TEST_MEETUP_NEXT_DESCRIPTION = "thenextbestmeetup_description"


def test_meetup():
    created = create_default_meetup()
    updated = update_default_meetup(created)
    delete_default_meetup(updated.get('id'))
    erase_default_meetup(updated.get('id'))

def update_default_meetup(updatable):

    updatable['name'] = TEST_MEETUP_NEXT_NAME

    response = requests.put(url_test, data=updatable)
    assert response.status_code < 300
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_MEETUP_NEXT_NAME
    assert updated.get('deleted') == False
    return updated

def create_default_meetup():
    return create_default_meetup_for_name(TEST_MEETUP_NAME)

def create_default_meetup_for_name(name: str):
    start_at = time.ctime()
    duration = 15
    meetup_template = create_default_meetup_template()
    org = create_default_org()
    facility = create_default_facility()
    meetup_spot = create_default_meetup_spot()
    crew = create_default_crew()

    response = requests.post(url_test, data={
        'name': name,
        'meetup_template_id': meetup_template.get('id'),
        'org_id': org.get('id'),
        'facility_id': facility.get('id'),
        'meetup_spot_id': meetup_spot.get('id'),
        'crew_id': crew.get('id'),
        'start_at': datetime.datetime.now()
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('name') == name
    assert created.get('meetup_template') == str(meetup_template.get('id'))
    assert created.get('org') == org.get('id')
    assert created.get('facility') == facility.get('id')
    assert created.get('meetup_spot') == meetup_spot.get('id')
    assert created.get('crew') == crew.get('id')
    assert not created.get('deleted')
    return created

def erase_default_meetup(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300


def delete_default_meetup(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')
