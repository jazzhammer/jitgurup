import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def createSpotType():
    response = requests.post(f"{API_BASE_URL}/tests/reset/spot_type")
    response = requests.post(f"{API_BASE_URL}/spot_types", json={
        "name": "anothername",
        "description": "anotherdescription"
    })
    responseJson = response.json();
    created = responseJson['created']
    assert created is not None
    assert created['name'] == "anothername"
    assert created['description'] == "anotherdescription"
    return created

def getSpotType(SpotType):
    response = requests.get(f"{API_BASE_URL}/spot_type/{SpotType['id']}")
    SpotTypeJson = response.json()
    assert SpotTypeJson is not None
    assert SpotTypeJson['name'] == SpotType['name']
    assert SpotTypeJson['description'] == SpotType['description']
    assert SpotTypeJson['id'] == SpotType['id']
    return SpotTypeJson

def getSpotTypeByName(SpotType):
    response = requests.get(f"{API_BASE_URL}/spot_types?name={SpotType['name']}")
    responseJson = response.json()
    SpotTypeJson = responseJson['matched']
    assert SpotTypeJson is not None
    assert SpotTypeJson['name'] == SpotType['name']
    assert SpotTypeJson['description'] == SpotType['description']
    assert SpotTypeJson['id'] == SpotType['id']
    return SpotTypeJson

def testAll():
    created = createSpotType()
    getSpotType(created)
    getSpotTypeByName(created)
