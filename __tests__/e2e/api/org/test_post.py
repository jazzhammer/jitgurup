import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def resetTests():
    response = requests.post(
        f"{API_BASE_URL}/tests/reset/org"
    )
    # assert response.status_code < 300, f"failure: {response.status_code}, {response.json()}"


def createOrg():
    resetTests()
    response = requests.post(
        f"{API_BASE_URL}/orgs",
        json={
            "name": "testname",
            "description": "testdescription"
        }
    )
    json = response.json()
    created = json['created']
    assert created != None;
    assert created['name'] == 'testname'
    assert created['description'] == 'testdescription'
    return created

def getOrg(org):
    response = requests.get(
        f"{API_BASE_URL}/orgs/{org['id']}"
    )
    orgJson = response.json()
    assert orgJson['name'] == "testname"
    assert orgJson['description'] == 'testdescription'

def testAll():
    created = createOrg()
    getOrg(created)

