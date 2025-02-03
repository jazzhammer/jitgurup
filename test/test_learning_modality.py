import json

import requests


url_test = 'http://localhost:8000/api/learning_modalitys'

TEST_LEARNING_MODALITY_NAME = "thebest_learning_modality_name"
TEST_LEARNING_MODALITY_NEXT_NAME = "thenextbest_learning_modality_name"

def test_learning_modality():
    created = create_default_learning_modality()
    updated = update_default_learning_modality(created)
    delete_default_learning_modality(created.get('id'))
    erase_default_learning_modality(created.get('id'))

def update_default_learning_modality(updatable):
    updatable['name'] = TEST_LEARNING_MODALITY_NEXT_NAME
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_LEARNING_MODALITY_NEXT_NAME
    assert updated.get('deleted') == False

def get_learning_modality_for_name(name: str):
    response = requests.get(url_test, params={
        'name': name
    })
    return json.loads(response.content.decode('utf-8'))

def delete_learning_modality(learning_modality):
    response = requests.delete(url_test, params={
        'id': learning_modality.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_learning_modality():

    # learning_modality_template = create_default_learning_modality_template()
    return create_default_learning_modality_for_name(TEST_LEARNING_MODALITY_NAME)

def create_default_learning_modality_for_name(name: str):
    response = requests.post(url_test, data={
        'name': name
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert not created.get('deleted')
        return created

def erase_default_learning_modality(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300



def delete_default_learning_modality(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

