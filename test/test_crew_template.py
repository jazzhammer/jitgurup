import json

import requests

url_test = 'http://localhost:8000/api/crew_templates'

TEST_CREW_TEMPLATE_NAME = "thebestcrew_template"
TEST_CREW_TEMPLATE_NEXT_NAME = "thenextbestcrew_template"
def test_crew_template():
    created = create_default_crew_template()
    updated = update_default_crew_template(created, TEST_CREW_TEMPLATE_NEXT_NAME)
    delete_default_crew_template(created.get('id'))

def update_default_crew_template(updatable, next_name):
    updatable['name'] = next_name
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == next_name
    assert updated.get('deleted') == False

def create_default_crew_template():
    return create_default_crew_template_for_name(TEST_CREW_TEMPLATE_NAME)

def create_default_crew_template_for_name(name: str):
    response = requests.post(url_test, data={
        'name': name
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('name') == name
    assert not created.get('deleted')
    return created

def delete_default_crew_template(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

