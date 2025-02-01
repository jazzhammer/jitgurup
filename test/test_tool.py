import json

import requests

url_test = 'http://localhost:8000/api/tools'

TEST_TOOL_NAME = "thebesttool"
TEST_TOOL_NEXT_NAME = "thenextbesttool"
def test_tool():
    created = create_default_tool()
    updated = update_default_tool(created, TEST_TOOL_NEXT_NAME)
    delete_default_tool(created.get('id'))
    erase_default_tool(created.get('id'))

def update_default_tool(updatable, next_name):
    updatable['name'] = next_name
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('name') == next_name
    assert updated.get('deleted') == False

def create_default_tool():
    response = requests.post(url_test, data={
        'name': TEST_TOOL_NAME
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    assert created.get('name') == TEST_TOOL_NAME
    assert not created.get('deleted')
    return created

def erase_default_tool(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))

def delete_default_tool(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

