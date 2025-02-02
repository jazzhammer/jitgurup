import json

import requests

from test_crew_template import erase_default_crew_template

from test_org import erase_default_org

from test_facility import erase_default_facility

from test_meetup_spot import erase_default_meetup_spot

from test_spot_type import erase_default_spot_type
from test_prereq_set import create_default_prereq_set, create_default_prereq_set_for_template, erase_default_prereq_set
from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name, \
    erase_default_meetup_template

url_test = 'http://localhost:8000/api/prereq_details'

TEST_PREREQ_DETAIL_SET_NAME = "thebestprereq_detail"
TEST_PREREQ_DETAIL_SET_NEXT_NAME = "thenextbestprereq_detail"

def test_prereq_detail():
    (   created,
        meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
        prereq_set,
        meetup_template2,
        crew_template2,
        org2,
        facility23,
        meetup_spot2,
        facility3,
        org4,
        spot_type2,
        org5,
    ) = create_default_prereq_detail()
    (
        updated,
        meetup_templateu,
        prereq_setu,
        crew_templateu,
        orgu,
        facilityu,
        meetup_spotu,
        facilityu,
        orgu,
        spot_typeu,
        orgu,
    ) = update_default_prereq_detail(created)
    delete_default_prereq_detail(created.get('id'))
    erase_default_prereq_detail(created.get('id'))

    erase_default_prereq_set(prereq_set.get('id'))
    erase_default_prereq_set(prereq_setu.get('id'))

    erase_default_meetup_template(meetup_template.get('id'))
    erase_default_meetup_template(meetup_template2.get('id'))
    erase_default_meetup_template(meetup_templateu.get('id'))

    erase_default_crew_template(crew_template.get('id'))
    erase_default_crew_template(crew_template2.get('id'))
    erase_default_crew_template(crew_templateu.get('id'))


    erase_default_org(org.get('id'))
    erase_default_org(org2.get('id'))
    erase_default_org(org3.get('id'))
    erase_default_org(org2.get('id'))
    erase_default_org(org4.get('id'))
    erase_default_org(org5.get('id'))

    erase_default_meetup_spot(meetup_spot.get('id'))
    erase_default_meetup_spot(meetup_spot2.get('id'))

    erase_default_facility(facility.get('id'))
    erase_default_facility(facility2.get('id'))
    erase_default_facility(facility23.get('id'))
    erase_default_facility(facility3.get('id'))

    erase_default_spot_type(spot_type.get('id'))
    erase_default_spot_type(spot_type2.get('id'))

    erase_default_meetup_spot(meetup_spotu.get('id'))

    erase_default_facility(facilityu.get('id'))
    erase_default_facility(facilityu.get('id'))

    erase_default_org(orgu.get('id'))
    erase_default_org(orgu.get('id'))
    erase_default_org(orgu.get('id'))

    erase_default_spot_type(spot_typeu.get('id'))


def update_default_prereq_detail(updatable):
    (
        next_meetup_template,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3
    ) = create_default_meetup_template_for_name('another name')
    next_prereq_set = create_default_prereq_set_for_template(next_meetup_template)

    updatable['template_id'] = next_meetup_template.get('id')
    updatable['prereq_set_id'] = next_prereq_set.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('template') == next_meetup_template.get('id')
    assert updated.get('prereq_set') == next_prereq_set.get('id')
    assert updated.get('deleted') == False
    return (
        updated,
        next_meetup_template,
        next_prereq_set,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
    )

def create_default_prereq_detail():
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
    (
        prereq_set,
        meetup_template2,
        crew_template2,
        org2,
        facility2,
        meetup_spot2,
        facility3,
        org4,
        spot_type2,
        org5,
    ) = create_default_prereq_set()
    response = requests.post(url_test, data={
        'template_id': meetup_template.get('id'),
        'prereq_set_id': prereq_set.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('template') == meetup_template.get('id')
        assert created.get('prereq_set') == prereq_set.get('id')
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
            prereq_set,
            meetup_template2,
            crew_template2,
            org2,
            facility2,
            meetup_spot2,
            facility3,
            org4,
            spot_type2,
            org5,
        )

def erase_default_prereq_detail(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


def delete_default_prereq_detail(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

