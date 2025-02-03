import json

import requests

from test_crew_template import erase_default_crew_template

from test_org import erase_default_org

from test_facility import erase_default_facility

from test_meetup_spot import erase_default_meetup_spot

from test_spot_type import erase_default_spot_type
from test_subject import erase_default_subject
from test_meetup_template import create_default_meetup_template, create_default_meetup_template_for_name, \
    erase_default_meetup_template
from test_topic import create_default_topic, create_default_topic_for_name, erase_default_topic

url_test = 'http://localhost:8000/api/template_topics'


def test_template_topic():
    (
        created,
        topic,
        subject,
        meetup_templateu,
        crew_templateu,
        orgu,
        facilityu,
        meetup_spotu,
        facility2u,
        org2u,
        spot_typeu,
        org3u,
    ) = create_default_template_topic()
    (
        updated,
        next_topic,
        next_meetup_template,
        subject2,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3,
    ) = update_default_template_topic(created)
    delete_default_template_topic(created.get('id'))

    erase_default_template_topic(created.get('id'))

    erase_default_topic(next_topic.get('id'))
    erase_default_topic(topic.get('id'))

    erase_default_meetup_template(next_meetup_template.get('id'))
    erase_default_subject(subject.get('id'))

    erase_default_meetup_template(meetup_templateu.get('id'))
    erase_default_crew_template(crew_templateu.get('id'))
    erase_default_crew_template(crew_template.get('id'))

    erase_default_meetup_spot(meetup_spot.get('id'))
    erase_default_meetup_spot(meetup_spotu.get('id'))
    erase_default_spot_type(spot_typeu.get('id'))
    erase_default_spot_type(spot_type.get('id'))

    erase_default_facility(facility2u.get('id'))
    erase_default_facility(facilityu.get('id'))
    erase_default_facility(facility.get('id'))
    erase_default_facility(facility2.get('id'))

    erase_default_org(orgu.get('id'))
    erase_default_org(org2u.get('id'))
    erase_default_org(org3u.get('id'))
    erase_default_org(org2.get('id'))
    erase_default_org(org3.get('id'))
    erase_default_org(org.get('id'))


def update_default_template_topic(updatable):
    next_topic, subject = create_default_topic_for_name('another name')
    (next_meetup_template,
     crew_template,
     org,
     facility,
     meetup_spot,
     facility2,
     org2,
     spot_type,
     org3,) = create_default_meetup_template_for_name('another template')

    updatable['topic_id'] = next_topic.get('id')
    updatable['meetup_template_id'] = next_meetup_template.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('topic') == next_topic.get('id')
    assert updated.get('meetup_template') == next_meetup_template.get('id')
    assert updated.get('deleted') == False
    return (
        updated,
        next_topic,
        next_meetup_template,
        subject,
        crew_template,
        org,
        facility,
        meetup_spot,
        facility2,
        org2,
        spot_type,
        org3
    )


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
    topic, subject = create_default_topic()
    (
        meetup_templateu,
        crew_templateu,
        orgu,
        facilityu,
        meetup_spotu,
        facility2u,
        org2u,
        spot_typeu,
        org3u
    ) = create_default_meetup_template()
    response = requests.post(url_test, data={
        'topic_id': topic.get('id'),
        'meetup_template_id': meetup_templateu.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('topic') == topic.get('id')
        assert created.get('meetup_template') == meetup_templateu.get('id')
        assert not created.get('deleted')
        return (
            created,
            topic,
            subject,
            meetup_templateu,
            crew_templateu,
            orgu,
            facilityu,
            meetup_spotu,
            facility2u,
            org2u,
            spot_typeu,
            org3u,
        )


def erase_default_template_topic(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


def delete_default_template_topic(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

