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
    assert updated.get('first_name').lower() == TEST_PERSON_NEXT_NAME.lower()
    assert updated.get('last_name').lower() == TEST_PERSON_NEXT_LAST_NAME.lower()
    assert updated.get('deleted') == False

def create_default_person():
    return create_default_person_for_names(TEST_PERSON_NAME, TEST_PERSON_LAST_NAME)

def erase_default_person():
    return erase_default_person_for_names(TEST_PERSON_NAME, TEST_PERSON_LAST_NAME)

def create_default_person_for_names(first_name: str, last_name: str):
    response = requests.post(url_test, data={
        'first_name': first_name,
        'last_name': last_name
    })

    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('first_name').lower() == first_name.lower()
    assert created.get('last_name').lower() == last_name.lower()
    assert not created.get('deleted')
    return created


def erase_default_person_for_names(first_name: str, last_name: str):
    response = requests.get(url_test, params={
        'first_name': first_name,
        'last_name': last_name
    })
    if response.status_code < 300:
        founds = json.loads(response.content.decode('utf8'))
        for found in founds:
            requests.delete(url_test, params={'id': found.get('id'), 'erase': True})


def delete_default_person(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')
