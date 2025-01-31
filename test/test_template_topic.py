import json

import requests

from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name
from test_topic import create_default_topic, create_default_topic_for_name

url_test = 'http://localhost:8000/api/template_topics'


def test_template_topic():
    created = create_default_template_topic()
    updated = update_default_template_topic(created)
    delete_default_template_topic(created.get('id'))

def update_default_template_topic(updatable):
    next_topic = create_default_topic_for_name('another name')
    next_meetup_template = create_default_meetup_template_for_name('another template')
    updatable['topic_id'] = next_topic.get('id')
    updatable['meetup_template_id'] = next_meetup_template.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('topic') == next_topic.get('id')
    assert updated.get('meetup_template') == next_meetup_template.get('id')
    assert updated.get('deleted') == False

def get_template_topic_for_name_topic(name: str, topic: int):
    response = requests.get(url_test, params={
        'name': name,
        'topic_id': topic
    })
    return json.loads(response.content.decode('utf-8'))

def delete_template_topic(template_topic):
    response = requests.delete(url_test, params={
        'id': template_topic.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_template_topic():
    topic = create_default_topic()
    meetup_template = create_default_meetup_template()
    response = requests.post(url_test, data={
        'topic_id': topic.get('id'),
        'meetup_template_id': meetup_template.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('topic') == topic.get('id')
        assert created.get('meetup_template') == meetup_template.get('id')
        assert not created.get('deleted')
        return created

def delete_default_template_topic(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

