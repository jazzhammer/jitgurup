import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def resetTests():
    response = requests.post(
        f"{API_BASE_URL}/tests/reset/users/preference"
    )
    assert response.status_code < 300, f"failure: {response.status_code}, {response.json()}"

def getUser():
    response = requests.post(f"{API_BASE_URL}/users", {
        "username": "gorgonhasspoken",
        "password": "ilovehammertime"
    })
    json = response.json()
    if 'authenticated' in json:
        authenticated = json['authenticated']
        if authenticated is None:
            return createUser()
        else:
            return authenticated
    else:
        return createUser()

def createUser():
    resetTests()
    response = requests.post(
        f"{API_BASE_URL}/users",
        json={
            "last_name": "gorgon III",
            "first_name": "luis",
            "username": "gorgonhasspoken",
            "password": "ilovehammertime",
            "email": "live@jazzhammer.com"
        }
    )
    json = response.json()
    created = json['created']
    assert created is not None
    assert created['last_name'] == 'gorgon III'
    assert created['first_name'] == 'luis'
    assert created['email'] == 'live@jazzhammer.com'
    return created

def createUserPreference(user, name, value):
    response = requests.post(f"{API_BASE_URL}/users/preference", json={
        "user_id": user['id'],
        "name": name,
        "value": value
    })
    json = response.json()
    created = json['created']
    assert created is not None
    assert created['user_id'] == user['id']
    assert created['name'] == name
    assert created['value'] == value
    return created

def validUserPreference(user, preference, name, value):
    assert preference['name'] == name
    assert preference['value'] == value
    response = requests.get(f"{API_BASE_URL}/users/preference?user_id={user['id']}")
    userPreferencesJson = response.json()
    assert userPreferencesJson is not None

def testAll():
    user = getUser()
    userPreference = createUserPreference(user, 'somepreference', 'somevalue')
    validUserPreference(user, userPreference, 'somepreference', 'somevalue')
# resetTests()
# testAll()
# print(get_response.status_code)
# print(get_response.json())
