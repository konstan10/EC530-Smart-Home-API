import pytest
from smarthomeapi import app

house_info = {'id': 1, 'name': 'Myles', 'address': '610 Beacon St'}
floor_info = {'id': 1, 'name': 'Ninth Floor'}
room_info = {'id': 1, 'name': 'My Dorm'}

@pytest.fixture
def client():
    """Set up a test client for testing"""
    with app.test_client() as client:
        yield client

def test_create_house(client):
    response = client.post('/houses', json=house_info)
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'House created:' in response_data
    assert 'Myles' in response_data
    assert '610 Beacon St' in response_data

def test_create_floor(client):
    client.post('/houses', json=house_info)
    
    response = client.post('/houses/1/floors', json=floor_info)
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'Floor created:' in response_data
    assert 'Ninth Floor' in response_data

def test_create_room(client):
    client.post('/houses', json=house_info)
    client.post('/houses/1/floors', json=floor_info)
    
    response = client.post('/floors/1/rooms', json=room_info)
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'Room created:' in response_data
    assert 'My Dorm' in response_data

def test_delete_house(client):
    client.post('/houses', json=house_info)
    client.post('/houses/1/floors', json=floor_info)
    client.post('/floors/1/rooms', json=room_info)

    response = client.delete('/houses/1')
    assert response.status_code == 200
    assert 'House deleted' in response.get_data(as_text=True)

    response = client.get('/houses/1')
    assert response.status_code == 404
    assert 'House not found' in response.get_data(as_text=True)

    response = client.get('/floors/1')
    assert response.status_code == 404
    assert 'Floor not found' in response.get_data(as_text=True)

    response = client.get('/rooms/1')
    assert response.status_code == 404
    assert 'Room not found' in response.get_data(as_text=True)
