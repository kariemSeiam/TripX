import pytest
from app import create_app
from app.extensions import db
from app.models import User, Vehicle
from flask_jwt_extended import create_access_token

import pytest

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()
    flask_app = create_app('testing')
    
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture
def user():
    user = User(username='testuser', email='testuser@example.com', phone_number='+1234567890')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

def get_jwt_headers(user):
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

def test_unauthorized_access(test_client):
    response = test_client.get('/vehicles')
    assert response.status_code == 401
    data = response.get_json()
    assert data['msg'] == 'Missing Authorization Header'

def test_add_vehicle(test_client, user):
    headers = get_jwt_headers(user)
    data = {
        'make': 'Toyota',
        'model': 'Camry',
        'year': 2020,
        'license_plate': 'ABC123'
    }
    response = test_client.post('/vehicles', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Vehicle added successfully'
    assert 'vehicle_id' in data

def test_get_vehicles(test_client, user):
    headers = get_jwt_headers(user)
    response = test_client.get('/vehicles', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_update_vehicle(test_client, user):
    vehicle = Vehicle(user_id=user.id, make='Honda', model='Civic', year=2019, license_plate='XYZ987')
    db.session.add(vehicle)
    db.session.commit()

    headers = get_jwt_headers(user)
    data = {
        'color': 'Blue'
    }
    response = test_client.put(f'/vehicles/{vehicle.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Vehicle updated successfully'

def test_delete_vehicle(test_client, user):
    vehicle = Vehicle(user_id=user.id, make='Ford', model='Fusion', year=2018, license_plate='LMN456')
    db.session.add(vehicle)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.delete(f'/vehicles/{vehicle.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Vehicle deleted successfully'
