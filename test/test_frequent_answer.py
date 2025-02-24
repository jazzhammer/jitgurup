import json

import requests

from test_frequent_question import create_default_frequent_question_for_content, create_default_frequent_question, erase_default_frequent_question

url_test = 'http://localhost:8000/api/frequent_answers'

TEST_FREQUENT_ANSWER_CONTENT = "thebest_frequent_answer_CONTENT"
TEST_FREQUENT_ANSWER_NEXT_CONTENT = "thenextbest_frequent_answer_CONTENT"

def test_frequent_answer():
    created, frequent_question = create_default_frequent_answer()
    updated, frequent_question2 = update_default_frequent_answer(created)
    delete_default_frequent_answer(created.get('id'))
    erase_default_frequent_answer(created.get('id'))
    erase_default_frequent_question(frequent_question.get('id'))
    erase_default_frequent_question(frequent_question2.get('id'))

def update_default_frequent_answer(updatable):
    next_frequent_question = create_default_frequent_question_for_content('another content')
    updatable['content'] = TEST_FREQUENT_ANSWER_NEXT_CONTENT
    updatable['frequent_question_id'] = next_frequent_question.get('id')
    response = requests.put(url_test, data={**updatable})
    assert response.status_code == 200
    updated = json.loads(response.content.decode('utf-8'))
    assert updated
    assert updated.get('content') == TEST_FREQUENT_ANSWER_NEXT_CONTENT
    assert updated.get('frequent_question') == next_frequent_question.get('id')
    assert updated.get('deleted') == False
    return updated, next_frequent_question

def get_frequent_answer_for_name_frequent_question(name: str, frequent_question: int):
    response = requests.get(url_test, params={
        'frequent_question_id': frequent_question
    })
    return json.loads(response.content.decode('utf-8'))

def delete_frequent_answer(frequent_answer):
    response = requests.delete(url_test, params={
        'id': frequent_answer.get('id')
    })
    assert response.status_code < 300
    deleted = json.loads(response.content.decode('utf-8'))
    assert deleted.get('deleted')
    return deleted

def create_default_frequent_answer():
    return create_default_frequent_answer_for_name_content(TEST_FREQUENT_ANSWER_CONTENT)

def create_default_frequent_answer_for_name_content(content: str):
    frequent_question = create_default_frequent_question()
    response = requests.post(url_test, data={
        'content': content,
        'frequent_question_id': frequent_question.get('id')
    })
    assert response.status_code < 300
    created = json.loads(response.content.decode('utf-8'))
    if created:
        assert created.get('content') == content
        assert created.get('frequent_question')['id'] == frequent_question.get('id')
        assert not created.get('deleted')
        return created, frequent_question

def erase_default_frequent_answer(id: int):
    response = requests.delete(url_test, params={
        'id': id,
        'erase': True
    })
    if response.status_code >= 300:
        if response.status_code >= 400:
            if response.status_code >= 500:
                assert response.status_code < 500
            else:
                print(f"previously deleted: frequent_answer {id}")
        else:
            assert response.status_code < 300

def delete_default_frequent_answer(id: int):
    response = requests.delete(url_test, params={
        'id': id
    })
    assert response.status_code < 300
    detail = json.loads(response.content.decode('utf-8'))
    assert detail.get('deleted')

