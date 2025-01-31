import json

import requests

url_test = 'http://localhost:8000/api/villages'

TEST_VILLAGE_NAME = "thebestVILLAGE"
TEST_VILLAGE_NEXT_NAME = "thenextbestVILLAGE"

TEST_VILLAGE_DESCRIPTION = "thebestVILLAGE_DESCXRIPTION"
TEST_VILLAGE_NEXT_DESCRIPTION = "thebestVILLAGE_nextDESCRIPTION"


def test_village():
    created = create_default_village()
    updated = update_default_village(created)
    delete_default_village(created.get('id'))
    erase_default_village(created.get('id'))

def update_default_village(updatable):
    updatable['name'] = TEST_VILLAGE_NEXT_NAME
    updatable['description'] = TEST_VILLAGE_NEXT_DESCRIPTION
    response = requests.put(url_test, data=updatable)
    assert response.status_code < 300
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_VILLAGE_NEXT_NAME
    assert updated.get('description') == TEST_VILLAGE_NEXT_DESCRIPTION
    assert updated.get('deleted') == False

def create_default_village():
    return create_default_VILLAGE_for_name_description(TEST_VILLAGE_NAME, TEST_VILLAGE_DESCRIPTION)

def create_default_VILLAGE_for_name_description(name: str, description: str):
    response = requests.post(url_test, data={
        'name': name,
        'description': description
    })

    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert not created.get('deleted')
        return created


def erase_default_village(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300

def delete_default_village(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')
