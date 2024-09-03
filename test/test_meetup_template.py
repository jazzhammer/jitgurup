import json

import requests

url_test = 'http://localhost:8000/api/meetup_templates'

TEST_MEETUP_TEMPLATE_NAME = "thebestmeetup_template"
TEST_MEETUP_TEMPLATE_NEXT_NAME = "thenextbestmeetup_template"

def test_meetup_template():
    created = create_default_meetup_template()
    updated = update_default_meetup_template(created)
    delete_default_meetup_template(created.get('id'))

def update_default_meetup_template(updatable):
    updatable['name'] = TEST_MEETUP_TEMPLATE_NEXT_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_MEETUP_TEMPLATE_NEXT_NAME
    assert updated.get('deleted') == False

def create_default_meetup_template():
    response = requests.post(url_test, data={
        'name': TEST_MEETUP_TEMPLATE_NAME
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == TEST_MEETUP_TEMPLATE_NAME
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == TEST_MEETUP_TEMPLATE_NAME
        assert not created.get('deleted')
        return created

def delete_default_meetup_template(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

