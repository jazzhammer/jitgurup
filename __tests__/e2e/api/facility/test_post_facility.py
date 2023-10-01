import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def createFacility():
    response = requests.post(f"{API_BASE_URL}/tests/reset/facility")
    response = requests.post(f"{API_BASE_URL}/facilitys", json={
        "name": "anothername",
        "description": "anotherdescription",
        "org_id": "1"
    })
    responseJson = response.json();
    created = responseJson['created']
    assert created is not None
    assert created['name'] == "anothername"
    assert created['description'] == "anotherdescription"
    assert created['org_id'] == 1
    return created

def getFacility(facility):
    response = requests.get(f"{API_BASE_URL}/facility/{facility['id']}")
    facilityJson = response.json()
    assert facilityJson is not None
    assert facilityJson['name'] == facility['name']
    assert facilityJson['description'] == facility['description']
    assert facilityJson['id'] == facility['id']
    return facilityJson

def getFacilityByName(facility):
    response = requests.get(f"{API_BASE_URL}/facilitys?name={facility['name']}")
    responseJson = response.json()
    facilityJson = responseJson['matched']
    assert facilityJson is not None
    assert facilityJson['name'] == facility['name']
    assert facilityJson['description'] == facility['description']
    assert facilityJson['id'] == facility['id']
    return facilityJson

def getFacilitysByOrg(facility):
    response = requests.get(f"{API_BASE_URL}/facilitys?org_id={facility['org_id']}")
    responseJson = response.json()
    facilitysJson = responseJson['matched']
    assert facilitysJson is not None
    assert facilitysJson[0]['name'] == facility['name']
    assert facilitysJson[0]['description'] == facility['description']
    assert facilitysJson[0]['id'] == facility['id']
    return facilitysJson

def testAll():
    created = createFacility()
    getFacility(created)
    getFacilityByName(created)
    getFacilitysByOrg(created)