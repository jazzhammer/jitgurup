import requests

from __tests__.e2e.api.endpoint import API_BASE_URL

def testResetTests():
    print("person resetTests():")
    response = requests.post(
        f"{API_BASE_URL}/tests/reset"
    )
    assert response.status_code < 300, f"failure: {response.status_code}, {response.json()}"
def testAll():
    print("person testAll():")
    response = requests.post(
        f"{API_BASE_URL}/persons",
        json={
            "last_name": "ferdinand",
            "first_name": "alfonse"
        }
    )
    json = response.json()
    created = json['created']
    assert created != None;
    assert created['last_name'] == 'ferdinand'
    assert created['first_name'] == 'alfonse'

# resetTests()
# testAll()
# print(get_response.status_code)
# print(get_response.json())

