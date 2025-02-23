import json

import requests

url_test = 'http://localhost:8000/api/testimonys'

TEST_TESTIMONY_CONTENT = "thebesttestimony"
TEST_TESTIMONY_NEXT_CONTENT = "thenextbesttestimony"

TEST_TESTIMONY_TYPE = "thebesttestimony_TYPE"
TEST_TESTIMONY_NEXT_TYPE = "thenextbesttestimony_TYPE2"

TEST_TESTIMONY_URL = "thebesttestimony_URL"
TEST_TESTIMONY_NEXT_URL = "thenextbesttestimony_URL2"

def test_testimony():
    created = create_default_testimony()
    updated = update_default_testimony(created)
    delete_default_testimony(created.get('id'))
    erase_default_testimony(created.get('id'))

def update_default_testimony(updatable):
    updatable['content'] = TEST_TESTIMONY_NEXT_CONTENT
    updatable['type'] = TEST_TESTIMONY_NEXT_TYPE
    updatable['url'] = TEST_TESTIMONY_NEXT_URL
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('content') == TEST_TESTIMONY_NEXT_CONTENT
    assert updated.get('type') == TEST_TESTIMONY_NEXT_TYPE
    assert updated.get('url') == TEST_TESTIMONY_NEXT_URL
    assert updated.get('deleted') == False

def create_default_testimony():
    response = requests.post(url_test, data={
        'content': TEST_TESTIMONY_CONTENT,
        'type': TEST_TESTIMONY_TYPE,
        'url': TEST_TESTIMONY_URL
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('content') == TEST_TESTIMONY_CONTENT
        assert created.get('type') == TEST_TESTIMONY_TYPE
        assert created.get('url') == TEST_TESTIMONY_URL
        assert not created.get('deleted')
        return created

def erase_default_testimony(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))


def delete_default_testimony(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

