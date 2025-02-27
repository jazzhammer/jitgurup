import json

import requests

from test_person import erase_default_person

from test_crew import erase_default_crew

from test_meetup_role import erase_default_meetup_role

from test_user import erase_default_user

from test_meetup import erase_default_meetup

from test_meetup_template import erase_default_meetup_template

from test_crew_template import erase_default_crew_template

from test_org import erase_default_org

from test_facility import erase_default_facility

from test_meetup_spot import erase_default_meetup_spot

from test_spot_type import erase_default_spot_type
from test_signup import create_default_signup, erase_default_signup, create_default_signup_for_person_names

url_test = 'http://localhost:8000/api/focal_results'


def test_focal_result():
    (
    created,
    signup,
    person,
    crew,
    meetup_role,
    created_by,
    meetup,
    meetup_templatem,
    crew_templatem,
    orgm,
    facilitym,
    meetup_spotm,
    facility2m,
    org2m,
    spot_typem,
    org3m,
    org4m,
    facility3m,
    org5m,
    meetup_spot2m,
    crewm,
    facility4m,
    org6m,
    spot_type2m,
    created_by2,) = create_default_focal_result()
    (
        updated,
        signup3,
        person,
        crew,
        meetup_role,
        created_by,
        meetup,
        meetup_templatem,
        crew_templatem,
        orgm,
        facilitym,
        meetup_spotm,
        facility2m,
        org2m,
        spot_typem,
        org3m,
        org4m,
        facility3m,
        org5m,
        meetup_spot2m,
        crewm,
        facility4m,
        org6m,
        spot_type2m,
        created_by2
    )   = update_default_focal_result(created)
    delete_default_focal_result(created.get('id'))
    erase_default_focal_result(created.get('id'))
    erase_default_signup(signup.get('id'))
    erase_default_signup(signup3.get('id'))
    erase_default_person(person.get('id'))
    erase_default_crew(crew.get('id'))
    erase_default_meetup_role(meetup_role.get('id'))
    erase_default_user(created_by.get('id'))
    erase_default_meetup(meetup.get('id'))
    erase_default_meetup_template(meetup_templatem.get('id'))
    erase_default_crew_template(crew_templatem.get('id'))
    erase_default_org(orgm.get('id'))
    erase_default_facility(facilitym.get('id'))
    erase_default_meetup_spot(meetup_spotm.get('id'))
    erase_default_facility(facility2m.get('id'))
    erase_default_org(org2m.get('id'))
    erase_default_spot_type(spot_typem.get('id'))
    erase_default_org(org3m.get('id'))
    erase_default_org(org4m.get('id'))
    erase_default_facility(facility3m.get('id'))
    erase_default_org(org5m.get('id'))
    erase_default_meetup_spot(meetup_spot2m.get('id'))
    erase_default_crew(crewm.get('id'))
    erase_default_facility(facility4m.get('id'))
    erase_default_org(org6m.get('id'))
    erase_default_spot_type(spot_type2m.get('id'))
    if created_by2:
        erase_default_user(created_by2.get('id'))

def update_default_focal_result(updatable):
    (next_signup,
    person,
    crew,
    meetup_role,
    created_by,
    meetup,
    meetup_templatem,
    crew_templatem,
    orgm,
    facilitym,
    meetup_spotm,
    facility2m,
    org2m,
    spot_typem,
    org3m,
    org4m,
    facility3m,
    org5m,
    meetup_spot2m,
    crewm,
    facility4m,
    org6m,
    spot_type2m,
    created_by2) = create_default_signup_for_person_names('nextfirst', 'nextlast')
    updatable['signup_id'] = next_signup.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('signup') == next_signup.get('id')
    assert updated.get('deleted') == False
    return (updated,
            next_signup,
    person,
    crew,
    meetup_role,
    created_by,
    meetup,
    meetup_templatem,
    crew_templatem,
    orgm,
    facilitym,
    meetup_spotm,
    facility2m,
    org2m,
    spot_typem,
    org3m,
    org4m,
    facility3m,
    org5m,
    meetup_spot2m,
    crewm,
    facility4m,
    org6m,
    spot_type2m,
    created_by2,)

def get_focal_result_for_name_signup(name: str, signup: int):
    response = requests.get(url_test, params={
        'signup_id': signup
    })
    return json.loads(response.content.decode('utf-8'))

def delete_focal_result(focal_result):
    response = requests.delete(url_test, params={
        'id': focal_result.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_focal_result():
    (signup,
     person,
     crew,
     meetup_role,
     created_by,
     meetup,
     meetup_templatem,
     crew_templatem,
     orgm,
     facilitym,
     meetup_spotm,
     facility2m,
     org2m,
     spot_typem,
     org3m,
     org4m,
     facility3m,
     org5m,
     meetup_spot2m,
     crewm,
     facility4m,
     org6m,
     spot_type2m,
     created_by2,
     ) = create_default_signup()
    response = requests.post(url_test, data={
        'signup_id': signup.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('signup').get('id') == signup.get('id')
        assert not created.get('deleted')
        return (created,
                signup,
            person,
            crew,
            meetup_role,
            created_by,
            meetup,
            meetup_templatem,
            crew_templatem,
            orgm,
            facilitym,
            meetup_spotm,
            facility2m,
            org2m,
            spot_typem,
            org3m,
            org4m,
            facility3m,
            org5m,
            meetup_spot2m,
            crewm,
            facility4m,
            org6m,
            spot_type2m,
            created_by2,)

def erase_default_focal_result(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: focal_result {id}")
        else:
            assert response.status_code < 300

def delete_default_focal_result(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

