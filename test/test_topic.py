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
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_TOPIC_NEXT_NAME
    assert updated.get('deleted') == False

def create_default_topic():
    return create_default_topic_for_name(TEST_TOPIC_NAME)

def create_default_topic_for_name(name: str):
    subject = create_default_subject()
    response = requests.post(url_test, data={
        'name': name,
        'subject_id': subject.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert int(created.get('subject')) == int(subject.get('id'))
        assert not created.get('deleted')
        return created

def delete_default_topic(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

