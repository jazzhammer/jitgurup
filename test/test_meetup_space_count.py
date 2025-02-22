import json

import requests

from test_org import erase_default_org
from test_meetup_calculation import create_default_meetup_calculation, erase_default_meetup_calculation, \
    create_default_meetup_calculation_for

url_test = 'http://localhost:8000/api/meetup_space_counts'

TEST_MEETUP_SPACE_COUNT_MAX_PERSONS = 12
TEST_MEETUP_SPACE_COUNT_COUNT = 21
TEST_MEETUP_SPACE_COUNT_NEXT_MAX_PERSONS = 15
TEST_MEETUP_SPACE_COUNT_NEXT_COUNT = 13

NEXT_PUPIL_COUNT = 34
NEXT_GURU_COUNT = 34
NEXT_DAILY_MEETUP_INTERVAL_LENGTH = 34
NEXT_INTERMEETUP_TRANSITION = 34
NEXT_MAX_MEETUPS_PER_GURU_PER_DAY = 34
NEXT_TOTAL_GURU_MINUTES_PER_DAY = 34
NEXT_MAX_PUPIL_MEETUPS_PER_DAY = 34
NEXT_MINIMUM_PUPIL_MEETUPS_PER_DAY = 34


def test_meetup_space_count():
    created, meetup_calculation, org = create_default_meetup_space_count()
    updated, meetup_calculation2, org2 = update_default_meetup_space_count(created)
    delete_default_meetup_space_count(created.get('id'))
    erase_default_meetup_space_count(created.get('id'))
    erase_default_meetup_calculation(meetup_calculation.get('id'))
    erase_default_meetup_calculation(meetup_calculation2.get('id'))
    erase_default_org(org.get('id'))
    erase_default_org(org2.get('id'))

def update_default_meetup_space_count(updatable):
    next_meetup_calculation, org = create_default_meetup_calculation_for(
        NEXT_PUPIL_COUNT,
        NEXT_GURU_COUNT,
        NEXT_DAILY_MEETUP_INTERVAL_LENGTH,
        NEXT_INTERMEETUP_TRANSITION,
        NEXT_MAX_MEETUPS_PER_GURU_PER_DAY,
        NEXT_TOTAL_GURU_MINUTES_PER_DAY,
        NEXT_MAX_PUPIL_MEETUPS_PER_DAY,
        NEXT_MINIMUM_PUPIL_MEETUPS_PER_DAY
    )
    updatable['max_persons'] = TEST_MEETUP_SPACE_COUNT_NEXT_MAX_PERSONS
    updatable['count'] = TEST_MEETUP_SPACE_COUNT_NEXT_COUNT
    updatable['meetup_calculation_id'] = next_meetup_calculation.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert int(updated.get('max_persons')) == TEST_MEETUP_SPACE_COUNT_NEXT_MAX_PERSONS
    assert int(updated.get('count')) == TEST_MEETUP_SPACE_COUNT_NEXT_COUNT
    assert int(updated.get('meetup_calculation')) == next_meetup_calculation.get('id')
    assert updated.get('deleted') == False
    return updated, next_meetup_calculation, org

def get_meetup_space_count_for_max_persons_meetup_calculation(max_persons: int, meetup_calculation: int):
    response = requests.get(url_test, params={
        'max_persons': max_persons,
        'meetup_calculation_id': meetup_calculation
    })
    return json.loads(response.content.decode('utf-8'))

def delete_meetup_space_count(meetup_space_count):
    response = requests.delete(url_test, params={
        'id': meetup_space_count.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_meetup_space_count():
    return create_default_meetup_space_count_for(
        TEST_MEETUP_SPACE_COUNT_MAX_PERSONS,
        TEST_MEETUP_SPACE_COUNT_COUNT
    )

def create_default_meetup_space_count_for(max_persons: int, count: int):
    meetup_calculation, org = create_default_meetup_calculation()
    response = requests.post(url_test, data={
        'max_persons': max_persons,
        'count': count,
        'meetup_calculation_id': meetup_calculation.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert int(created.get('max_persons')) == max_persons
        assert int(created.get('count')) == count
        assert created.get('meetup_calculation_id') == meetup_calculation.get('id')
        assert not created.get('deleted')
        return created, meetup_calculation, org

def erase_default_meetup_space_count(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: meetup_space_count {id}")
        else:
            assert response.status_code < 300

def delete_default_meetup_space_count(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

