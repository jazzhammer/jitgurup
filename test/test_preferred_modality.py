import json
import requests

from test_subject import erase_default_subject
from test_topic import erase_default_topic, create_default_topic
from test_facility import create_default_facility

from test_learning_modality import create_default_learning_modality, erase_default_learning_modality
from test_person import create_default_person, erase_default_person

url_test = 'http://localhost:8000/api/preferred_modalitys'


def erase_default_learing_modality(param):
    pass


def test_preferred_modality():
    created, person, topic, subject, learning_modality = create_default_preferred_modality()

    delete_default_preferred_modality(created.get('id'))
    erase_default_person(person.get('id'))
    erase_default_topic(topic.get('id'))
    erase_default_subject(subject.get('id'))
    erase_default_learning_modality(learning_modality.get('id'))


def create_default_preferred_modality():
    person = create_default_person()
    topic, subject = create_default_topic()
    learning_modality = create_default_learning_modality()

    response = requests.post(url_test, data={
        'person_id': person.get('id'),
        'topic_id': topic.get('id'),
        'learning_modality_id': learning_modality.get('id'),
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('person_id') == person.get('id')
    assert created.get('topic_id') == topic.get('id')
    assert created.get('learning_modality_id') == learning_modality.get('id')
    assert not created.get('deleted')
    return (
        created,
        person,
        topic,
        subject,
        learning_modality,
    )

def delete_default_preferred_modality(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
