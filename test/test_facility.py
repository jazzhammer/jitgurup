import json

import requests

from test_org import create_default_org_for_name_description, create_default_org, erase_default_org

url_test = 'http://localhost:8000/api/facilitys'

TEST_FACILITY_NAME = "thebest_facility_name"
TEST_FACILITY_NEXT_NAME = "thenextbest_facility_name"
TEST_FACILITY_DESCRIPTION = "thebest_facility_DESCRIPTION"
TEST_FACILITY_NEXT_DESCRIPTION = "thenextbest_facility_DESCRIPTION"

def test_facility():
    created, org = create_default_facility()
    updated, org2 = update_default_facility(created)
    delete_default_facility(created.get('id'))
    erase_default_facility(created.get('id'))
    erase_default_org(org.get('id'))
    erase_default_org(org2.get('id'))

def update_default_facility(updatable):
    next_org = create_default_org_for_name_description('another name', 'another description')
    updatable['name'] = TEST_FACILITY_NEXT_NAME
    updatable['description'] = TEST_FACILITY_NEXT_DESCRIPTION
    updatable['org_id'] = next_org.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_FACILITY_NEXT_NAME
    assert updated.get('description') == TEST_FACILITY_NEXT_DESCRIPTION
    assert updated.get('org') == next_org.get('id')
    assert updated.get('deleted') == False
    return updated, next_org

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
    return create_default_facility_for_name_description(TEST_FACILITY_NAME, TEST_FACILITY_DESCRIPTION)

def create_default_facility_for_name_description(name: str, description: str):
    org = create_default_org()
    response = requests.post(url_test, data={
        'name': name,
        'description': description,
        'org_id': org.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert created.get('org') == org.get('id')
        assert not created.get('deleted')
        return created, org

def erase_default_facility(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: facility {id}")
        else:
            assert response.status_code < 300

def delete_default_facility(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

