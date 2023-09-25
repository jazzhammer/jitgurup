import requests

from __tests__.e2e.api.endpoint import API_BASE_URL

def testResetTests():
    response = requests.post(
        f"{API_BASE_URL}/tests/reset/security"
    )
    assert response.status_code < 300, f"failure: {response.status_code}, {response.json()}"
def testAll():
    response = requests.post(
        f"{API_BASE_URL}/users",
        json={
            "last_name": "gorgon III",
            "first_name": "luis",
            "username": "gorgonhasspoken",
            "password": "ilovetospeak",
            "email": "live@jazzhammer.com"
        }
    )
    json = response.json()
    created = json['created']
    assert created != None;
    assert created['last_name'] == 'gorgon III'
    assert created['first_name'] == 'luis'
    assert created['email'] == 'live@jazzhammer.com'

# resetTests()
# testAll()
# print(get_response.status_code)
# print(get_response.json())

