import json

import requests

from test_subject import create_default_subject

url_test = 'http://localhost:8000/api/topics'

TEST_TOPIC_NAME = "thebesttopic"
TEST_TOPIC_NEXT_NAME = "thenextbesttopic"

def test_topic():
    created = create_default_topic()
    updated = update_default_topic(created)
    delete_default_topic(created.get('id'))

def update_default_topic(updatable):
    updatable['name'] = TEST_TOPIC_NEXT_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    detail = json.loads(response.content.decode('utf-8'))
    updated = detail.get('updated')
    assert updated
    assert updated.get('name') == TEST_TOPIC_NEXT_NAME
    assert updated.get('deleted') == False

def create_default_topic():
    subject = create_default_subject()
    response = requests.post(url_test, data={
        'name': TEST_TOPIC_NAME,
        'subject_id': subject.get('id')
    })
    assert response.status_code < 300
    details = json.loads(response.content.decode('utf-8'))
    created = details.get('created')
    updated = details.get('updated')
    if updated:
        assert updated.get('name') == TEST_TOPIC_NAME
        assert updated.get('subject_id') == subject.get('id')
        assert not updated.get('deleted')
        return updated
    if created:
        assert created.get('name') == TEST_TOPIC_NAME
        assert created.get('subject') == subject.get('id')
        assert not created.get('deleted')
        return created

def delete_default_topic(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted').get('deleted')

