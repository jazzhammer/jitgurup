import json

import requests

url_test = 'http://localhost:8000/api/orgs'

TEST_ORG_NAME = "thebestorg"
TEST_ORG_NEXT_NAME = "thenextbestorg"


def test_org():
    created = create_default_org()
    updated = update_default_org(created)
    delete_default_org(created.get('id'))


def update_default_org(updatable):
    updatable['name'] = TEST_ORG_NEXT_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_ORG_NEXT_NAME
    assert updated.get('deleted') == False

def create_default_org():
    return create_default_org_for_name(TEST_ORG_NAME)

def create_default_org_for_name(name: str):
    response = requests.post(url_test, data={
        'name': name
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == name
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == name
        assert not created.get('deleted')
        return created


def delete_default_org(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')
