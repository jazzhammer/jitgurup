import json

import requests

url_test = 'http://localhost:8000/api/focal_artifact_types'

TEST_FOCAL_ARTIFACT_TYPE_NAME = "thebest_focal_artifact_type_name"
TEST_FOCAL_ARTIFACT_TYPE_NEXT_NAME = "thenextbest_focal_artifact_type_name"
TEST_FOCAL_ARTIFACT_TYPE_DESCRIPTION = "thebest_focal_artifact_type_DESCRIPTION"
TEST_FOCAL_ARTIFACT_TYPE_NEXT_DESCRIPTION = "thenextbest_focal_artifact_type_DESCRIPTION"

def test_focal_artifact_type():
    created = create_default_focal_artifact_type()
    updated = update_default_focal_artifact_type(created)
    delete_default_focal_artifact_type(created.get('id'))
    erase_default_focal_artifact_type(created.get('id'))

def update_default_focal_artifact_type(updatable):
    updatable['name'] = TEST_FOCAL_ARTIFACT_TYPE_NEXT_NAME
    updatable['description'] = TEST_FOCAL_ARTIFACT_TYPE_NEXT_DESCRIPTION
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == TEST_FOCAL_ARTIFACT_TYPE_NEXT_NAME
    assert updated.get('description') == TEST_FOCAL_ARTIFACT_TYPE_NEXT_DESCRIPTION
    assert updated.get('deleted') == False
    return updated

def get_focal_artifact_type_for_name(name: str, org: int):
    response = requests.get(url_test, params={
        'name': name
    })
    return json.loads(response.content.decode('utf-8'))

def delete_focal_artifact_type(focal_artifact_type):
    response = requests.delete(url_test, params={
        'id': focal_artifact_type.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_focal_artifact_type():
    return create_default_focal_artifact_type_for_name_description(TEST_FOCAL_ARTIFACT_TYPE_NAME, TEST_FOCAL_ARTIFACT_TYPE_DESCRIPTION)

def create_default_focal_artifact_type_for_name_description(name: str, description: str):
    response = requests.post(url_test, data={
        'name': name,
        'description': description
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('name') == name
        assert created.get('description') == description
        assert not created.get('deleted')
        return created

def erase_default_focal_artifact_type(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: focal_artifact_type {id}")
        else:
            assert response.status_code < 300

def delete_default_focal_artifact_type(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

