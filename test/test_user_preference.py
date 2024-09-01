import json

import requests

url_test = 'http://localhost:8000/api/users/preference'

TEST_PREFERENCE_NAME = "thebestuser_preference"
TEST_PREFERENCE_NEXT_NAME = "thenextbestuser_preference"
TEST_PREFERENCE_VALUE = "thebestuser_preference_VALUE"
TEST_PREFERENCE_NEXT_VALUE = "thenextbestuser_preference_VALUE"
TEST_PREFERENCE_USER_ID = 1
TEST_PREFERENCE_NEXT_USER_ID = 2

def test_user_preference():
    created = create_default_user_preference()
    updated = update_default_user_preference(created)
    delete_default_user_preference(created.get('id'))

def update_default_user_preference(updatable):
    updatable['name'] = TEST_PREFERENCE_NEXT_NAME
    updatable['user_id'] = TEST_PREFERENCE_NEXT_USER_ID
    updatable['value'] = TEST_PREFERENCE_NEXT_VALUE
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_PREFERENCE_NEXT_NAME
    assert updated.get('user') == TEST_PREFERENCE_NEXT_USER_ID
    assert updated.get('value') == TEST_PREFERENCE_NEXT_VALUE
    assert updated.get('deleted') == False

def create_default_user_preference():
    response = requests.post(url_test, data={
        'name': TEST_PREFERENCE_NAME,
        'value': TEST_PREFERENCE_VALUE,
        'user_id': TEST_PREFERENCE_USER_ID
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == TEST_PREFERENCE_NAME
        assert updated.get('value') == TEST_PREFERENCE_VALUE
        assert updated.get('user') == TEST_PREFERENCE_USER_ID
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == TEST_PREFERENCE_NAME
        assert created.get('value') == TEST_PREFERENCE_VALUE
        assert created.get('user') == TEST_PREFERENCE_USER_ID
        assert not created.get('deleted')
        return created

def delete_default_user_preference(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

