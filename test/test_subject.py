import json

import requests

url_test = 'http://localhost:8000/api/subjects'

TEST_SUBJECT_NAME = "thebestsubject"
TEST_SUBJECT_NEXT_NAME = "thenextbestsubject"

def test_subject():
    created = create_default_subject()
    updated = update_default_subject(created)
    delete_default_subject(created.get('id'))

def update_default_subject(updatable):
    updatable['name'] = TEST_SUBJECT_NEXT_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_SUBJECT_NEXT_NAME
    assert updated.get('deleted') == False

def create_default_subject():
    response = requests.post(url_test, data={
        'name': TEST_SUBJECT_NAME
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == TEST_SUBJECT_NAME
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == TEST_SUBJECT_NAME
        assert not created.get('deleted')
        return created

def delete_default_subject(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

