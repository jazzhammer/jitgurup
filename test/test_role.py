import json

import requests

url_test = 'http://localhost:8000/api/roles'

TEST_ROLE_NAME = "thebestrole"
TEST_ROLE_NEXT_NAME = "thenextbestrole"

def test_role():
    created = create_default_role()
    updated = update_default_role(created, TEST_ROLE_NEXT_NAME)
    delete_default_role(created.get('id'))

def update_default_role(updatable, next_name):
    updatable['name'] = next_name
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == next_name
    assert updated.get('deleted') == False

def create_default_role():
    response = requests.post(url_test, data={
        'name': TEST_ROLE_NAME
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('name') == TEST_ROLE_NAME
    assert not created.get('deleted')
    return created

def delete_default_role(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')

