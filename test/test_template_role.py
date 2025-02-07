import json

import requests

from test_crew_template import create_default_crew_template_for_name, create_default_crew_template

url_test = 'http://localhost:8000/api/template_roles'

TEST_TEMPLATE_ROLE_NAME = "thebest_template_role_name"
TEST_TEMPLATE_ROLE_NEXT_NAME = "thenextbest_template_role_name"
TEST_TEMPLATE_ROLE_DESCRIPTION = "thebest_template_role_DESCRIPTION"
TEST_TEMPLATE_ROLE_NEXT_DESCRIPTION = "thenextbest_template_role_DESCRIPTION"

def test_template_role():
    created = create_default_template_role()
    updated = update_default_template_role(created)
    delete_default_template_role(created.get('id'))
    erase_template_role(created.get('id'))

def update_default_template_role(updatable):
    next_crew_template = create_default_crew_template_for_name('another name')
    updatable['name'] = TEST_TEMPLATE_ROLE_NEXT_NAME
    updatable['description'] = TEST_TEMPLATE_ROLE_NEXT_DESCRIPTION
    updatable['crew_template_id'] = next_crew_template.get('id')
    response = requests.put(url_test, data=updatable)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_TEMPLATE_ROLE_NEXT_NAME
    assert updated.get('description') == TEST_TEMPLATE_ROLE_NEXT_DESCRIPTION
    assert updated.get('crew_template') == next_crew_template.get('id')
    assert updated.get('deleted') == False

def get_template_role_for_name_crew_template(name: str, crew_template: int):
    response = requests.get(url_test, params={
        'name': name,
        'crew_template_id': crew_template
    })
    return json.loads(response.content.decode('utf-8'))

def delete_template_role(template_role):
    response = requests.delete(url_test, params={
        'id': template_role.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_template_role():
    return create_default_template_role_for_name_description(TEST_TEMPLATE_ROLE_NAME, TEST_TEMPLATE_ROLE_DESCRIPTION)

def create_default_template_role_for_name_description(name: str, description: str):
    crew_template = create_default_crew_template()
    matches = get_template_role_for_name_crew_template(TEST_TEMPLATE_ROLE_NAME, crew_template.get('id'))
    for match in matches:
        delete_template_role(match)

    response = requests.post(url_test, data={
        'name': name,
        'description': description,
        'crew_template_id': crew_template.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert created.get('crew_template') == crew_template.get('id')
        assert not created.get('deleted')
        return created

def delete_default_template_role(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

def erase_template_role(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

