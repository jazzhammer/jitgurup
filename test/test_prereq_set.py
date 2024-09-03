import json

import requests

from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name

url_test = 'http://localhost:8000/api/prereq_sets'

TEST_PREREQ_SET_NAME = "thebestprereq_set"
TEST_PREREQ_SET_NEXT_NAME = "thenextbestprereq_set"

def test_prereq_set():
    created = create_default_prereq_set()
    updated = update_default_prereq_set(created)
    delete_default_prereq_set(created.get('id'))

def update_default_prereq_set(updatable):
    next_meetup_template = create_default_meetup_template_for_name('another name')
    updatable['required_by_id'] = next_meetup_template.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('required_by') == next_meetup_template.get('id')
    assert updated.get('deleted') == False

def create_default_prereq_set():
    meetup_template = create_default_meetup_template()
    response = requests.post(url_test, data={
        'required_by_id': meetup_template.get('id')
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('required_by') == meetup_template.get('id')
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('required_by') == meetup_template.get('id')
        assert not created.get('deleted')
        return created

def delete_default_prereq_set(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

