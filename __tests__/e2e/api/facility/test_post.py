import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def createFacility():
    response = requests.post(f"{API_BASE_URL}/facilitys", json={
        "name": "anothername",
        "description": "anotherdescription"
    })
    responseJson = response.json();
    created = responseJson['created']
    assert created is not None
    assert created['name'] == "anothername"
    assert created['description'] == "anotherdescription"
    return created

def getFacility(facility):
    response = requests.get(f"{API_BASE_URL}/facility/{facility['id']}")
    facilityJson = response.json()
    assert facilityJson is not None
    assert facilityJson['name'] == facility['name']
    assert facilityJson['description'] == facility['description']
    return facilityJson

def getFacilityByName(facility):
    response = requests.get(f"{API_BASE_URL}/facilitys?name={facility['name']}")
    responseJson = response.json()
    facilityJson = responseJson['matched']
    assert facilityJson is not None
    assert facilityJson['name'] == facility['name']
    assert facilityJson['description'] == facility['description']
    return facilityJson

def testAll():
    created = createFacility()
    getFacility(created)
    getFacilityByName(created)