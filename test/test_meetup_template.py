import json

import requests

from test_facility import create_default_facility_for_name_description
from test_org import create_default_org, create_default_org_for_name_description

from test_meetup_spot import create_default_meetup_spot, create_default_meetup_spot_for_name_description
from test_crew_template import create_default_crew_template_for_name, create_default_crew_template

url_test = 'http://localhost:8000/api/meetup_templates'

TEST_MEETUP_TEMPLATE_NAME = "thebestmeetup_template"
TEST_MEETUP_TEMPLATE_NEXT_NAME = "thenextbestmeetup_template"


def test_meetup_template():
    created = create_default_meetup_template()
    updated = update_default_meetup_template(created)
    delete_default_meetup_template(created.get('id'))

def update_default_meetup_template(updatable):
    crew_template = create_default_crew_template_for_name('another crew template')
    org = create_default_org_for_name_description('another org', 'another org description')
    facility = create_default_facility_for_name_description('another facility', 'another facility description')
    meetup_spot = create_default_meetup_spot_for_name_description('another meetup_spot', 'another meetup-spot description')
    next_work_in_progress = not updatable['work_in_progress']
    updatable['name'] = TEST_MEETUP_TEMPLATE_NEXT_NAME
    updatable['crew_template_id'] = crew_template.get('id')
    updatable['org_id'] = org.get('id')
    updatable['facility_id'] = facility.get('id')
    updatable['meetup_spot_id'] = meetup_spot.get('id')
    updatable['work_in_progress'] = next_work_in_progress
    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_MEETUP_TEMPLATE_NEXT_NAME
    assert updated.get('crew_template') == crew_template.get('id')
    assert updated.get('org') == org.get('id')
    assert updated.get('facility') == facility.get('id')
    assert updated.get('meetup_spot') == meetup_spot.get('id')
    assert updated.get('work_in_progress') == next_work_in_progress
    assert updated.get('deleted') == False

def create_default_meetup_template():
    return create_default_meetup_template_for_name(TEST_MEETUP_TEMPLATE_NAME)

def create_default_meetup_template_for_name(name: str):
    crew_template = create_default_crew_template()
    org = create_default_org()
    facility = create_default_org()
    meetup_spot = create_default_meetup_spot()

    response = requests.post(url_test, data={
        'name': name,
        'crew_template_id': crew_template.get('id'),
        'org_id': org.get('id'),
        'facility_id': facility.get('id'),
        'meetup_spot_id': meetup_spot.get('id'),
        'work_in_progress': False
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == name
        assert updated.get('crew_template') == crew_template.get('id')
        assert updated.get('org') == org.get('id')
        assert updated.get('facility') == facility.get('id')
        assert updated.get('meetup_spot') == meetup_spot.get('id')
        assert updated.get('work_in_progress') == False
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == name
        assert created.get('crew_template') == crew_template.get('id')
        assert created.get('org') == org.get('id')
        assert created.get('facility') == facility.get('id')
        assert created.get('meetup_spot') == meetup_spot.get('id')
        assert created.get('work_in_progress') == False
        assert not created.get('deleted')
        return created


def delete_default_meetup_template(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')
