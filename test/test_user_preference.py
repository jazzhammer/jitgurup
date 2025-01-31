import json

import requests

url_test = 'http://localhost:8000/api/users/preference'

TEST_PREFERENCE_NAME = "thebestuser_preference"
TEST_PREFERENCE_NEXT_NAME = "thenextbestuser_preference"
TEST_PREFERENCE_VALUE = "thebestuser_preference_VALUE"
TEST_PREFERENCE_NEXT_VALUE = "thenextbestuser_preference_VALUE"
TEST_PREFERENCE_USER_ID = 1
TEST_PREFERENCE_NEXT_USER_ID = 2

from test_user import create_default_user_for_names, erase_user

def test_user_preference():
    created, created_by = create_default_user_preference()
    updated, updated_by = update_default_user_preference(created)
    delete_default_user_preference(created.get('id'))
    erase_default_user_preference(created.get('id'))

    erase_user(created_by.get('username'))
    erase_user(updated_by.get('username'))

def update_default_user_preference(updatable):
    next_user = create_default_user_for_names('next first', 'next last', 'nextusername')
    updatable['name'] = TEST_PREFERENCE_NEXT_NAME
    updatable['user_id'] = next_user.get('id')
    updatable['value'] = TEST_PREFERENCE_NEXT_VALUE
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_PREFERENCE_NEXT_NAME
    assert updated.get('user') == next_user.get('id')
    assert updated.get('value') == TEST_PREFERENCE_NEXT_VALUE
    assert updated.get('deleted') == False
    return updated, next_user

def create_default_user_preference():
    user = create_default_user_for_names('afirst', 'alast', 'ausername')
    response = requests.post(url_test, data={
        'name': TEST_PREFERENCE_NAME,
        'value': TEST_PREFERENCE_VALUE,
        'user_id': user.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))

    if created:
        assert created.get('name') == TEST_PREFERENCE_NAME
        assert created.get('value') == TEST_PREFERENCE_VALUE.lower()
        assert created.get('user') == user.get('id')
        assert not created.get('deleted')
        return created, user

def erase_default_user_preference(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300

def delete_default_user_preference(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

