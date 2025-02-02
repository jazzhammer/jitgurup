import datetime
import json
import time

import requests

from test_user import erase_default_user
from test_crew_template import erase_default_crew_template

from test_spot_type import erase_default_spot_type
from test_meetup_template import create_default_meetup_template, erase_default_meetup_template
from test_org import create_default_org, erase_default_org
from test_facility import create_default_facility, erase_default_facility
from test_meetup_spot import create_default_meetup_spot, erase_default_meetup_spot
from test_crew import create_default_crew, erase_default_crew

url_test = 'http://localhost:8000/api/meetups'

TEST_MEETUP_NAME = "thebestmeetup"
TEST_MEETUP_NEXT_NAME = "thenextbestmeetup"
TEST_MEETUP_DESCRIPTION = "thebestmeetup_description"
TEST_MEETUP_NEXT_DESCRIPTION = "thenextbestmeetup_description"


def test_meetup():
    (
        created,
        meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
        org4,
        facility3,
        org5,
        meetup_spot2,
        crew,
        facility4,
        org6,
        spot_type2,
        created_by2,
    ) = create_default_meetup()
    updated = update_default_meetup(created)

    delete_default_meetup(updated.get('id'))
    erase_default_meetup(updated.get('id'))
    if created_by2:
        erase_default_user(created_by2.get('id'))

    erase_default_meetup_template(meetup_template.get('id'))
    erase_default_crew_template(crew_template.get('id'))
    erase_default_meetup_spot(meetup_spot.get('id'))
    erase_default_meetup_spot(meetup_spot2.get('id'))

    erase_default_facility(facility.get('id'))
    erase_default_facility(facility2.get('id'))
    erase_default_facility(facility3.get('id'))
    erase_default_facility(facility4.get('id'))

    erase_default_org(org.get('id'))
    erase_default_org(org2.get('id'))
    erase_default_org(org3.get('id'))
    erase_default_org(org4.get('id'))
    erase_default_org(org5.get('id'))
    erase_default_org(org6.get('id'))

    erase_default_spot_type(spot_type.get('id'))
    erase_default_spot_type(spot_type2.get('id'))
    erase_default_crew(crew.get('id'))


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
    (
        meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
     ) = create_default_meetup_template()
    org4 = create_default_org()
    facility3, org5 = create_default_facility()
    (
        meetup_spot2,
        facility4,
        org6,
        spot_type2,
    ) = create_default_meetup_spot()
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
    return (
        created,
        meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
        org4,
        facility3,
        org5,
        meetup_spot2,
        crew,
        facility4,
        org6,
        spot_type2,
        None, # created by, not needed here, but must return
    )

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
