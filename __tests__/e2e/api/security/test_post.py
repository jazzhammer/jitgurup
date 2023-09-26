import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def resetTests():
    response = requests.post(
        f"{API_BASE_URL}/tests/reset/security"
    )
    assert response.status_code < 300, f"failure: {response.status_code}, {response.json()}"


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
    assert created != None;
    assert created['last_name'] == 'gorgon III'
    assert created['first_name'] == 'luis'
    assert created['email'] == 'live@jazzhammer.com'


def findUsername():
    resetTests()
    createUser()
    response = requests.post(
        f"{API_BASE_URL}/users",
        json={
            "username": "gorgonhasspoken",
        }
    )
    json = response.json()
    matched = json['matched']
    assert matched is not None
    assert matched["last_name"] == "gorgon III"
    assert matched["first_name"] == "luis"
    assert matched["username"] == "gorgonhasspoken"
    assert matched["email"] == "live@jazzhammer.com"


def authenticate():
    resetTests()
    createUser()
    response = requests.post(
        f"{API_BASE_URL}/users",
        json={
            "username": "gorgonhasspoken",
            "password": "ilovehammertime"
        }
    )
    json = response.json()
    matched = json['authenticated']
    assert matched is not None
    assert matched["last_name"] == "gorgon III"
    assert matched["first_name"] == "luis"
    assert matched["username"] == "gorgonhasspoken"
    assert matched["email"] == "live@jazzhammer.com"

def testAll():
    authenticate()
    # findUsername()
    # createUser()

# resetTests()
# testAll()
# print(get_response.status_code)
# print(get_response.json())
