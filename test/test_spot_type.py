import json

import requests

url_test = 'http://localhost:8000/api/spot_types'

TEST_SPOT_TYPE_NAME = "thebestspot_type"
TEST_SPOT_TYPE_NEXT_NAME = "thenextbestspot_type"

TEST_SPOT_TYPE_DESCRIPTION = "thebestspot_type_DESCXRIPTION"
TEST_SPOT_TYPE_NEXT_DESCRIPTION = "thebestspot_type_nextDESCRIPTION"


def test_spot_type():
    created = create_default_spot_type()
    updated = update_default_spot_type(created)
    delete_default_spot_type(created.get('id'))


def update_default_spot_type(updatable):
    updatable['name'] = TEST_SPOT_TYPE_NEXT_NAME
    updatable['description'] = TEST_SPOT_TYPE_NEXT_DESCRIPTION
    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_SPOT_TYPE_NEXT_NAME
    assert updated.get('description') == TEST_SPOT_TYPE_NEXT_DESCRIPTION
    assert updated.get('deleted') == False

def create_default_spot_type():
    return create_default_spot_type_for_name_description(TEST_SPOT_TYPE_NAME, TEST_SPOT_TYPE_DESCRIPTION)

def create_default_spot_type_for_name_description(name: str, description: str):
    response = requests.post(url_test, data={
        'name': name,
        'description': description
    })

    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == name
        assert updated.get('description') == description
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert not created.get('deleted')
        return created


def delete_default_spot_type(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')
