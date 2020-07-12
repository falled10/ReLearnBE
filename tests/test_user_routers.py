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
def test_create_new_user_with_the_same_telegram_id(client, user):
    data = {
        'telegram_id': user['telegram_id'],
        'username': 'something-else'
    }
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
def test_get_current_user(client, user):
    resp = client.get(f'/api/users/me', headers={'Authorization': user['telegram_id']})
    assert resp.status_code == 200
    assert resp.json()['telegramId'] == user['telegram_id']


@pytest.mark.asyncio
def test_get_non_existed_user(client):
    resp = client.get('/api/users/me', headers={'Authorization': 'dfadfsasdf'})
    assert resp.status_code == 401


@pytest.mark.asyncio
def test_get_current_user_without_authorization_header(client):
    resp = client.get('/api/users/me')
    assert resp.status_code == 401
