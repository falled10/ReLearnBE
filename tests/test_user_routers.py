import pytest


@pytest.mark.asyncio
def test_create_new_user(client):
    data = {
        'telegram_id': 'something',
        'username': 'something-else'
    }
    resp = client.post('/api/users', json=data)
    assert resp.status_code == 200
    assert resp.json()['username'] == data['username']


@pytest.mark.asyncio
def test_create_new_user_with_the_same_telegram_id(client):
    data = {
        'telegram_id': 'something',
        'username': 'something-else'
    }
    client.post('/api/users', json=data)
    resp = client.post('/api/users', json=data)
    assert resp.status_code == 400


@pytest.mark.asyncio
def test_create_new_user_without_telegram_id(client):
    data = {
        'username': 'something'
    }
    resp = client.post('/api/users', json=data)
    assert resp.status_code == 400


@pytest.mark.asyncio
def test_get_user_by_its_id(client):
    data = {
        'telegram_id': 'something',
        'username': 'something-else'
    }
    client.post('/api/users', json=data)
    resp = client.get(f'/api/users/{data["telegram_id"]}')
    print(resp.json())
    assert resp.status_code == 200
    assert resp.json()['telegramId'] == data['telegram_id']


@pytest.mark.asyncio
def test_get_non_existed_user(client):
    resp = client.get('/api/users/adsfadsfadsf')
    assert resp.status_code == 404
