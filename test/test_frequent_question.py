import json

import requests

url_test = 'http://localhost:8000/api/frequent_questions'

TEST_FREQUENT_QUESTION_CONTENT = "thebest_frequent_question_CONTENT"
TEST_FREQUENT_QUESTION_NEXT_CONTENT = "thenextbest_frequent_question_CONTENT"

def test_frequent_question():
    created = create_default_frequent_question()
    updated = update_default_frequent_question(created)
    delete_default_frequent_question(created.get('id'))
    erase_default_frequent_question(created.get('id'))

def update_default_frequent_question(updatable):
    updatable['content'] = TEST_FREQUENT_QUESTION_NEXT_CONTENT
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('content') == TEST_FREQUENT_QUESTION_NEXT_CONTENT
    assert updated.get('deleted') == False
    return updated

def get_frequent_question_for_content(content: str, org: int):
    response = requests.get(url_test, params={
        'content': content
    })
    return json.loads(response.content.decode('utf-8'))

def delete_frequent_question(frequent_question):
    response = requests.delete(url_test, params={
        'id': frequent_question.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_frequent_question():
    return create_default_frequent_question_for_content(TEST_FREQUENT_QUESTION_CONTENT)

def create_default_frequent_question_for_content(content: str):
    response = requests.post(url_test, data={
        'content': content,
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('content') == content
        assert not created.get('deleted')
        return created

def erase_default_frequent_question(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: frequent_question {id}")
        else:
            assert response.status_code < 300

def delete_default_frequent_question(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

