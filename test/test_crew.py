import json

import requests

from test_crew_template import create_default_crew_template, create_default_crew_template_for_name

url_test = 'http://localhost:8000/api/crews'

TEST_CREW_NAME = "thebest_crew_name"
TEST_CREW_NEXT_NAME = "thenextbest_crew_name"

def test_crew():
    created = create_default_crew()
    updated = update_default_crew(created)
    delete_default_crew(created.get('id'))
    erase_default_crew(created.get('id'))

def update_default_crew(updatable):
    next_crew_template = create_default_crew_template_for_name('next crew template name')
    updatable['name'] = TEST_CREW_NEXT_NAME
    updatable['crew_template_id'] = next_crew_template.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_CREW_NEXT_NAME
    assert updated.get('deleted') == False

def get_crew_for_name(name: str):
    response = requests.get(url_test, params={
        'name': name
    })
    return json.loads(response.content.decode('utf-8'))

def delete_crew(crew):
    response = requests.delete(url_test, params={
        'id': crew.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_crew():

    # crew_template = create_default_crew_template()
    return create_default_crew_for_name(TEST_CREW_NAME)

def create_default_crew_for_name(name: str):
    matches = get_crew_for_name(TEST_CREW_NAME)
    for match in matches:
        delete_crew(match)

    response = requests.post(url_test, data={
        'name': name
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert not created.get('deleted')
        return created

def erase_default_crew(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


def delete_default_crew(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

