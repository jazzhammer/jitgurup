import json

import requests

from test_crew_template import erase_default_crew_template

from test_org import erase_default_org

from test_facility import erase_default_facility

from test_meetup_spot import erase_default_meetup_spot

from test_spot_type import erase_default_spot_type
from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name, \
    erase_default_meetup_template

url_test = 'http://localhost:8000/api/prereq_sets'

TEST_PREREQ_SET_NAME = "thebestprereq_set"
TEST_PREREQ_SET_NEXT_NAME = "thenextbestprereq_set"

def test_prereq_set():
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
    ) = create_default_prereq_set()
    (
        updated,
        next_meetup_templateu,
        crew_templateu,
        orgu,
        facilityu,
        meetup_spotu,
        facility2u,
        org2u,
        spot_typeu,
        org3u,
    ) = update_default_prereq_set(created)
    delete_default_prereq_set(created.get('id'))
    erase_default_prereq_set(created.get('id'))

    erase_default_meetup_template(meetup_template.get('id'))
    erase_default_meetup_template(next_meetup_templateu.get('id'))

    erase_default_meetup_spot(meetup_spot.get('id'))
    erase_default_meetup_spot(meetup_spotu.get('id'))

    erase_default_facility(facility.get('id'))
    erase_default_facility(facility2.get('id'))
    erase_default_facility(facilityu.get('id'))
    erase_default_facility(facility2u.get('id'))

    erase_default_org(org.get('id'))
    erase_default_org(org2.get('id'))
    erase_default_org(org3.get('id'))
    erase_default_org(orgu.get('id'))
    erase_default_org(org2u.get('id'))
    erase_default_org(org3u.get('id'))

    erase_default_crew_template(crew_template.get('id'))
    erase_default_crew_template(crew_templateu.get('id'))
    erase_default_spot_type(spot_type.get('id'))

    erase_default_spot_type(spot_typeu.get('id'))

def update_default_prereq_set(updatable):
    (
        next_meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
    ) = create_default_meetup_template_for_name('another name')

    updatable['required_by_id'] = next_meetup_template.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('required_by') == next_meetup_template.get('id')
    assert updated.get('deleted') == False
    return (
        updated,
        next_meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
    )

def create_default_prereq_set():
    (
        meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3
    ) = create_default_meetup_template()
    created = create_default_prereq_set_for_template(meetup_template)
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
    )


def create_default_prereq_set_for_template(meetup_template):
    response = requests.post(url_test, data={
        'required_by_id': meetup_template.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('required_by') == meetup_template.get('id')
        assert not created.get('deleted')
        return created

def erase_default_prereq_set(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))

def delete_default_prereq_set(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

