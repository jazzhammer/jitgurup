import requests

from __tests__.e2e.api.endpoint import API_BASE_URL


def createMeetupSpot():
    response = requests.post(f"{API_BASE_URL}/tests/reset/meetup_spot")
    response = requests.post(f"{API_BASE_URL}/meetup_spots", json={
        "name": "anothername",
        "description": "anotherdescription",
        "spot_type_id": "0",
        "facility_id": "1"
    })
    responseJson = response.json();
    assert 'created' in responseJson
    created = responseJson['created']
    assert created is not None
    assert created['name'] == "anothername"
    assert created['description'] == "anotherdescription"
    assert created['facility_id'] == 1
    assert created['spot_type_id'] == 0
    return created

def getMeetupSpot(MeetupSpot):
    response = requests.get(f"{API_BASE_URL}/meetup_spot/{MeetupSpot['id']}")
    MeetupSpotJson = response.json()
    assert MeetupSpotJson is not None
    assert MeetupSpotJson['name'] == MeetupSpot['name']
    assert MeetupSpotJson['description'] == MeetupSpot['description']
    assert MeetupSpotJson['id'] == MeetupSpot['id']
    assert MeetupSpotJson['facility_id'] == MeetupSpot['facility_id']
    assert MeetupSpotJson['spot_type_id'] == MeetupSpot['spot_type_id']
    return MeetupSpotJson

def getMeetupSpotByName(MeetupSpot):
    response = requests.get(f"{API_BASE_URL}/meetup_spots?name={MeetupSpot['name']}")
    responseJson = response.json()
    MeetupSpotJson = responseJson['matched']
    assert MeetupSpotJson is not None
    assert MeetupSpotJson['name'] == MeetupSpot['name']
    assert MeetupSpotJson['description'] == MeetupSpot['description']
    assert MeetupSpotJson['id'] == MeetupSpot['id']
    assert MeetupSpotJson['facility_id'] == MeetupSpot['facility_id']
    assert MeetupSpotJson['spot_type_id'] == MeetupSpot['spot_type_id']
    return MeetupSpotJson

def getMeetupSpotsByFacility(MeetupSpot):
    response = requests.get(f"{API_BASE_URL}/meetup_spots?facility_id={MeetupSpot['facility_id']}")
    responseJson = response.json()
    MeetupSpotsJson = responseJson['matched']
    assert MeetupSpotsJson is not None
    assert MeetupSpotsJson[0]['name'] == MeetupSpot['name']
    assert MeetupSpotsJson[0]['description'] == MeetupSpot['description']
    assert MeetupSpotsJson[0]['id'] == MeetupSpot['id']
    assert MeetupSpotsJson[0]['facility_id'] == MeetupSpot['facility_id']
    assert MeetupSpotsJson[0]['spot_type_id'] == MeetupSpot['spot_type_id']
    return MeetupSpotsJson

def testAll():
    created = createMeetupSpot()
    getMeetupSpot(created)
    getMeetupSpotByName(created)
    getMeetupSpotsByFacility(created)