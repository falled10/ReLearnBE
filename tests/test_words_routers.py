import pytest


@pytest.mark.asyncio
def test_get_one_random_word(client, random_word):
    resp = client.get('/api/words/random_word')
    assert resp.status_code == 200
    assert 'id' in resp.json()['word']
    assert 'word' in resp.json()
    assert 'variants' in resp.json()
    assert resp.json()['word']['word'] in resp.json()['variants']


@pytest.mark.asyncio
def test_send_answer(client, random_word, user):
    words = random_word.inserted_ids
    data = {
        'word_id': str(words[0])
    }
    resp = client.post('/api/words/answer', json=data, headers={'Authorization': user['telegram_id']})

    assert resp.status_code == 204

    user_resp = client.get(f'/api/users/{user["telegram_id"]}')

    assert user_resp.status_code == 200
    assert data['word_id'] in user_resp.json()['words']
