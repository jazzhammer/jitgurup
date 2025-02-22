import json

import requests

from test_org import create_default_org, erase_default_org

url_test = 'http://localhost:8000/api/meetup_calculations'

PUPIL_COUNT = 3
GURU_COUNT = 3
DAILY_MEETUP_INTERVAL_LENGTH = 3
INTERMEETUP_TRANSITION = 3
MAX_MEETUPS_PER_GURU_PER_DAY = 3
TOTAL_GURU_MINUTES_PER_DAY = 3
MAX_PUPIL_MEETUPS_PER_DAY = 3
MINIMUM_PUPIL_MEETUPS_PER_DAY = 3

NEXT_PUPIL_COUNT = 7
NEXT_GURU_COUNT = 7
NEXT_DAILY_MEETUP_INTERVAL_LENGTH = 7
NEXT_INTERMEETUP_TRANSITION = 7
NEXT_MAX_MEETUPS_PER_GURU_PER_DAY = 7
NEXT_TOTAL_GURU_MINUTES_PER_DAY = 7
NEXT_MAX_PUPIL_MEETUPS_PER_DAY = 7
NEXT_MINIMUM_PUPIL_MEETUPS_PER_DAY = 7

def test_meetup_calculation():

    created, org = create_default_meetup_calculation()
    updated = update_default_meetup_calculation(created)
    delete_default_meetup_calculation(created.get('id'))
    erase_default_meetup_calculation(created.get('id'))
    erase_default_org(org.get('id'))


def update_default_meetup_calculation(updatable):

    updatable['pupil_count'] = PUPIL_COUNT
    updatable['guru_count'] = GURU_COUNT
    updatable['daily_meetup_interval_length'] = DAILY_MEETUP_INTERVAL_LENGTH
    updatable['intermeetup_transition'] = INTERMEETUP_TRANSITION
    updatable['max_meetups_per_guru_per_day'] = MAX_MEETUPS_PER_GURU_PER_DAY
    updatable['total_guru_minutes_per_day'] = TOTAL_GURU_MINUTES_PER_DAY
    updatable['max_pupil_meetups_per_day'] = MAX_PUPIL_MEETUPS_PER_DAY
    updatable['minimum_pupil_meetups_per_day'] = MINIMUM_PUPIL_MEETUPS_PER_DAY

    response = requests.put(url_test, data=updatable)
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert int(updated.get('pupil_count')) == PUPIL_COUNT
    assert int(updated.get('guru_count')) == GURU_COUNT
    assert int(updated.get('daily_meetup_interval_length')) == DAILY_MEETUP_INTERVAL_LENGTH
    assert int(updated.get('intermeetup_transition')) == INTERMEETUP_TRANSITION
    assert int(updated.get('max_meetups_per_guru_per_day')) == MAX_MEETUPS_PER_GURU_PER_DAY
    assert int(updated.get('total_guru_minutes_per_day')) == TOTAL_GURU_MINUTES_PER_DAY
    assert int(updated.get('max_pupil_meetups_per_day')) == MAX_PUPIL_MEETUPS_PER_DAY
    assert int(updated.get('minimum_pupil_meetups_per_day')) == MINIMUM_PUPIL_MEETUPS_PER_DAY

    return updated

def get_meetup_calculation_for_name_meetup_calculation(name: str, meetup_calculation: int):
    response = requests.get(url_test, params={
        'name': name,
        'meetup_calculation_id': meetup_calculation
    })
    return json.loads(response.content.decode('utf-8'))

def delete_meetup_calculation(meetup_calculation):
    response = requests.delete(url_test, params={
        'id': meetup_calculation.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_meetup_calculation():
    return create_default_meetup_calculation_for(
        PUPIL_COUNT,
        GURU_COUNT,
        DAILY_MEETUP_INTERVAL_LENGTH,
        INTERMEETUP_TRANSITION,
        MAX_MEETUPS_PER_GURU_PER_DAY,
        TOTAL_GURU_MINUTES_PER_DAY,
        MAX_PUPIL_MEETUPS_PER_DAY,
        MINIMUM_PUPIL_MEETUPS_PER_DAY
    )

def create_default_meetup_calculation_for(
    pupil_count,
    guru_count,
    daily_meetup_interval_length,
    intermeetup_transition,
    max_meetups_per_guru_per_day,
    total_guru_minutes_per_day,
    max_pupil_meetups_per_day,
    minimum_pupil_meetups_per_day
):
    org = create_default_org()
    response = requests.post(url_test, data={
        "pupil_count": pupil_count,
        "guru_count": guru_count,
        "daily_meetup_interval_length": daily_meetup_interval_length,
        "intermeetup_transition": intermeetup_transition,
        "max_meetups_per_guru_per_day": max_meetups_per_guru_per_day,
        "total_guru_minutes_per_day": total_guru_minutes_per_day,
        "max_pupil_meetups_per_day": max_pupil_meetups_per_day,
        "minimum_pupil_meetups_per_day": minimum_pupil_meetups_per_day
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert int(created.get("pupil_count")) == pupil_count
        assert int(created.get("guru_count")) == guru_count
        assert int(created.get("daily_meetup_interval_length")) == daily_meetup_interval_length
        assert int(created.get("intermeetup_transition")) == intermeetup_transition
        assert int(created.get("max_meetups_per_guru_per_day")) == max_meetups_per_guru_per_day
        assert int(created.get("total_guru_minutes_per_day")) == total_guru_minutes_per_day
        assert int(created.get("max_pupil_meetups_per_day")) == max_pupil_meetups_per_day
        assert int(created.get("minimum_pupil_meetups_per_day")) == minimum_pupil_meetups_per_day

        assert not created.get('deleted')
        return created, org

def erase_default_meetup_calculation(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: meetup_calculation {id}")
        else:
            assert response.status_code < 300

def delete_default_meetup_calculation(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


