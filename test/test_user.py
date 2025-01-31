import json

import requests

url_test = 'http://localhost:8000/api/users'

TEST_USER_NAME = "thebestuser"
TEST_USER_NEXT_NAME = "thenextbestuser"
TEST_USER_LAST_NAME = "thebestuser_LAST_NAME"
TEST_USER_NEXT_LAST_NAME = "thenextbestuser_LAST_NAME"

TEST_USER_USERNAME = "LIL old username"
TEST_USER_NEXT_USERNAME = "LIL old username_next"

def test_user():
    created = create_default_user()
    # updated = update_default_user(created)
    erase_default_user()


# def update_default_user(updatable):
#     updatable['first_name'] = TEST_USER_NEXT_NAME
#     updatable['last_name'] = TEST_USER_NEXT_LAST_NAME
#     response = requests.put(url_test, data=updatable)
#     assert response.status_code < 300
#     detail = json.loads(response.content.decode('utf-8'))
#     updated = detail.get('updated')
#     assert updated
#     assert updated.get('first_name').lower() == TEST_USER_NEXT_NAME.lower()
#     assert updated.get('last_name').lower() == TEST_USER_NEXT_LAST_NAME.lower()
#     assert updated.get('deleted') == False

def get_default_user():
    response = requests.get(url_test, params={'username': TEST_USER_USERNAME})
    try:
        return json.loads(response.content.decode('utf8'))
    except Exception as get_e:
        return None

def create_default_user():
    return create_default_user_for_names(TEST_USER_NAME, TEST_USER_LAST_NAME, TEST_USER_USERNAME)

def create_default_user_for_names(first_name: str, last_name: str, username: str):
    response = requests.post(url_test, data={
        'first_name': first_name,
        'last_name': last_name,
        'username': username
    })

    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('first_name').lower() == first_name.lower()
        assert created.get('last_name').lower() == last_name.lower()
        assert created.get('username').lower() == username.lower()
        assert not created.get('deleted')
        return created


def erase_user(username: str):
    response = requests.get(url_test, params={
        'username': username
    })
    founds = json.loads(response.content.decode('utf8'))

    for found in founds:
        response = requests.delete(url_test, params={
            'id': found.get('id'),
            'erase': True
        })
def erase_default_user():
    response = requests.get(url_test, params={
        'username': TEST_USER_USERNAME
    })
    founds = json.loads(response.content.decode('utf8'))

    for found in founds:
        response = requests.delete(url_test, params={
            'id': found.get('id'),
            'erase': True
        })

def delete_default_user(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('updated').get('deleted')
