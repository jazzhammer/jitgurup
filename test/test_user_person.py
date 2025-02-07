import json
import requests

from test_user import erase_default_user, create_default_user
from test_person import create_default_person, erase_default_person

url_test = 'http://localhost:8000/api/users/persons'


def test_user_person():
    created, person, user = create_default_user_person()

    delete_default_user_person(created.get('id'))
    erase_default_user_person(created.get('id'))
    erase_default_person(person.get('id'))
    erase_default_user(user.get('id'))

def create_default_user_person():
    person = create_default_person()
    user = create_default_user()

    response = requests.post(url_test, data={
        'person_id': person.get('id'),
        'user_id': user.get('id'),
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('person') == person.get('id')
    assert created.get('user') == user.get('id')
    assert not created.get('deleted')
    return (
        created,
        person,
        user,
    )

def delete_default_user_person(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300

def erase_default_user_person(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
