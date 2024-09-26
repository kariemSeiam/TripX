import pytest
from app import create_app
from app.extensions import db
from app.models import User, Trip, Vehicle, Driver
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def test_client():
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

@pytest.fixture
def driver():
    driver = Driver(username='testdriver', email='testdriver@example.com', phone_number='+1234567890')
    driver.set_password('password')
    db.session.add(driver)
    db.session.commit()
    return driver

@pytest.fixture
def vehicle(driver):
    vehicle = Vehicle(driver_id=driver.id, make='Toyota', model='Camry', year=2020, license_plate='ABC123', color='Blue', vehicle_type='sedan')
    db.session.add(vehicle)
    db.session.commit()
    return vehicle

def get_jwt_headers(user):
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

def test_create_trip(test_client, user, vehicle):
    headers = get_jwt_headers(user)
    data = {
        'vehicle_id': vehicle.id,
        'start_location': '123 Main St',
        'end_location': '456 Elm St',
        'fare': 20.50
    }
    response = test_client.post('/trips', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Trip created successfully'
    assert 'trip_id' in data

def test_get_trips(test_client, user):
    headers = get_jwt_headers(user)
    response = test_client.get('/trips', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_update_trip(test_client, user, vehicle):
    trip = Trip(driver_id=vehicle.driver_id, rider_id=user.id, vehicle_id=vehicle.id, start_location='123 Main St', end_location='456 Elm St', fare=20.50)
    db.session.add(trip)
    db.session.commit()

    headers = get_jwt_headers(user)
    data = {
        'status': 'completed'
    }
    response = test_client.put(f'/trips/{trip.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Trip updated successfully'

def test_delete_trip(test_client, user, vehicle):
    trip = Trip(driver_id=vehicle.driver_id, rider_id=user.id, vehicle_id=vehicle.id, start_location='123 Main St', end_location='456 Elm St', fare=20.50)
    db.session.add(trip)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.delete(f'/trips/{trip.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Trip deleted successfully'
