import json

import requests

from test_org import create_default_org_for_name_description, create_default_org

url_test = 'http://localhost:8000/api/facilitys'

TEST_FACILITY_NAME = "thebest_facility_name"
TEST_FACILITY_NEXT_NAME = "thenextbest_facility_name"
TEST_FACILITY_DESCRIPTION = "thebest_facility_DESCRIPTION"
TEST_FACILITY_NEXT_DESCRIPTION = "thenextbest_facility_DESCRIPTION"

def test_facility():
    created = create_default_facility()
    updated = update_default_facility(created)
    delete_default_facility(created.get('id'))

def update_default_facility(updatable):
    next_org = create_default_org_for_name_description('another name', 'another description')
    updatable['name'] = TEST_FACILITY_NEXT_NAME
    updatable['description'] = TEST_FACILITY_NEXT_DESCRIPTION
    updatable['org_id'] = next_org.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_FACILITY_NEXT_NAME
    assert updated.get('description') == TEST_FACILITY_NEXT_DESCRIPTION
    assert updated.get('org') == next_org.get('id')
    assert updated.get('deleted') == False

def get_facility_for_name_org(name: str, org: int):
    response = requests.get(url_test, params={
        'name': name,
        'org_id': org
    })
    return json.loads(response.content.decode('utf-8'))

def delete_facility(facility):
    response = requests.delete(url_test, params={
        'id': facility.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_facility():
    org = create_default_org()
    alreadys = get_facility_for_name_org(TEST_FACILITY_NAME, org.get('id'))
    matches = alreadys.get('matched')
    for match in matches:
        delete_facility(match)

    response = requests.post(url_test, data={
        'name': TEST_FACILITY_NAME,
        'description': TEST_FACILITY_DESCRIPTION,
        'org_id': org.get('id')
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == TEST_FACILITY_NAME
        assert updated.get('description') == TEST_FACILITY_DESCRIPTION
        assert updated.get('org') == org.get('id')
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == TEST_FACILITY_NAME
        assert created.get('description') == TEST_FACILITY_DESCRIPTION
        assert created.get('org') == org.get('id')
        assert not created.get('deleted')
        return created

def delete_default_facility(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

