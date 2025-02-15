import pytest
from smarthomeapi import app

@pytest.fixture
def client():
    """Set up a test client for testing"""
    with app.test_client() as client:
        yield client

def test_create_house(client):
    response = client.post('/houses', json={
        'id': 1, 
        'name': 'Myles',
        'address': '610 Beacon St'
    })
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'House created:' in response_data
    assert 'Myles' in response_data
    assert '610 Beacon St' in response_data

def test_create_floor(client):
    client.post('/houses', json={'id': 1, 'name': 'Myles', 'address': '610 Beacon St'})
    
    response = client.post('/houses/1/floors', json={'id': 1, 'name': 'Ninth Floor'})
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'Floor created:' in response_data
    assert 'Ninth Floor' in response_data

def test_create_room(client):
    client.post('/houses', json={'id': 1, 'name': 'Myles', 'address': '610 Beacon St'})
    client.post('/houses/1/floors', json={'id': 1, 'name': '9'})
    
    response = client.post('/floors/1/rooms', json={'id': 1, 'name': 'My Dorm'})
    assert response.status_code == 201
    response_data = response.get_data(as_text=True)
    assert 'Room created:' in response_data
    assert 'My Dorm' in response_data
