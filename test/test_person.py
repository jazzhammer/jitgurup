import json

import requests

url_test = 'http://localhost:8000/api/persons'

TEST_PERSON_NAME = "thebestperson"
TEST_PERSON_NEXT_NAME = "thenextbestperson"
TEST_PERSON_LAST_NAME = "thebestperson_LAST_NAME"
TEST_PERSON_NEXT_LAST_NAME = "thenextbestperson_LAST_NAME"

def test_person():
    created = create_default_person()
    updated = update_default_person(created)
    delete_default_person(created.get('id'))


def update_default_person(updatable):
    updatable['first_name'] = TEST_PERSON_NEXT_NAME
    updatable['last_name'] = TEST_PERSON_NEXT_LAST_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('first_name') == TEST_PERSON_NEXT_NAME
    assert updated.get('last_name') == TEST_PERSON_NEXT_LAST_NAME
    assert updated.get('deleted') == False

def create_default_person():
    return create_default_person_for_name_last_name(TEST_PERSON_NAME, TEST_PERSON_LAST_NAME)

def create_default_person_for_name_last_name(first_name: str, last_name: str):
    response = requests.post(url_test, data={
        'first_name': first_name,
        'last_name': last_name
    })

    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('first_name') == first_name
        assert updated.get('last_name') == last_name
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('first_name') == first_name
        assert created.get('last_name') == last_name
        assert not created.get('deleted')
        return created


def delete_default_person(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')
