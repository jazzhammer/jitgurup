import json

import requests

from test_spot_type import create_default_spot_type, create_default_spot_type_for_name_description

from test_facility import create_default_facility, create_default_facility_for_name_description

url_test = 'http://localhost:8000/api/meetup_spots'

TEST_MEETUP_SPOT_NAME = "thebestmeetup_spot"
TEST_MEETUP_SPOT_NEXT_NAME = "thenextbestmeetup_spot"
TEST_MEETUP_SPOT_DESCRIPTION = "thebestmeetup_spot_description"
TEST_MEETUP_SPOT_NEXT_DESCRIPTION = "thenextbestmeetup_spot_description"


def test_meetup_spot():
    created = create_default_meetup_spot()
    updated = update_default_meetup_spot(created)
    delete_default_meetup_spot(created.get('id'))
    erase_default_meetup_spot(created.get('id'))



def update_default_meetup_spot(updatable):
    spot_type = create_default_spot_type_for_name_description('next spot type', 'next spot type description')
    facility = create_default_facility_for_name_description('next spot type', 'next spot type description')

    updatable['name'] = TEST_MEETUP_SPOT_NEXT_NAME
    updatable['description'] = TEST_MEETUP_SPOT_NEXT_DESCRIPTION
    updatable['spot_type_id'] = spot_type.get('id')
    updatable['facility_id'] = facility.get('id')

    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_MEETUP_SPOT_NEXT_NAME
    assert updated.get('description') == TEST_MEETUP_SPOT_NEXT_DESCRIPTION
    assert updated.get('spot_type') == spot_type.get('id')
    assert updated.get('facility') == facility.get('id')
    assert updated.get('deleted') == False

def create_default_meetup_spot():
    return create_default_meetup_spot_for_name_description(TEST_MEETUP_SPOT_NAME, TEST_MEETUP_SPOT_DESCRIPTION)

def create_default_meetup_spot_for_name_description(name: str, description: str):
    spot_type = create_default_spot_type()
    facility = create_default_facility()
    response = requests.post(url_test, data={
        'name': name,
        'description': description,
        'spot_type_id': spot_type.get('id'),
        'facility_id': facility.get('id')
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == name
        assert updated.get('description') == description
        assert updated.get('spot_type') == spot_type.get('id')
        assert updated.get('facility') == facility.get('id')
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert created.get('spot_type') == spot_type.get('id')
        assert created.get('facility') == facility.get('id')
        assert not created.get('deleted')
        return created


def erase_default_meetup_spot(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))

def delete_default_meetup_spot(id: int):

    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')
