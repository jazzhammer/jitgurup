import json

import requests

from test_prereq_set import create_default_prereq_set, create_default_prereq_set_for_template
from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name

url_test = 'http://localhost:8000/api/prereq_details'

TEST_PREREQ_DETAIL_SET_NAME = "thebestprereq_detail"
TEST_PREREQ_DETAIL_SET_NEXT_NAME = "thenextbestprereq_detail"

def test_prereq_detail():
    created = create_default_prereq_detail()
    updated = update_default_prereq_detail(created)
    delete_default_prereq_detail(created.get('id'))

def update_default_prereq_detail(updatable):
    next_meetup_template = create_default_meetup_template_for_name('another name')
    next_prereq_set = create_default_prereq_set_for_template(next_meetup_template)

    updatable['template_id'] = next_meetup_template.get('id')
    updatable['prereq_set_id'] = next_prereq_set.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('template') == next_meetup_template.get('id')
    assert updated.get('prereq_set') == next_prereq_set.get('id')
    assert updated.get('deleted') == False

def create_default_prereq_detail():
    meetup_template = create_default_meetup_template()
    prereq_set = create_default_prereq_set()
    response = requests.post(url_test, data={
        'template_id': meetup_template.get('id'),
        'prereq_set_id': prereq_set.get('id')
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('template') == meetup_template.get('id')
        assert updated.get('prereq_set') == prereq_set.get('id')
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('template') == meetup_template.get('id')
        assert created.get('prereq_set') == prereq_set.get('id')
        assert not created.get('deleted')
        return created

def delete_default_prereq_detail(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

