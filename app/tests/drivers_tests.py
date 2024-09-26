import pytest
from app import create_app
from app.extensions import db
from app.models import User, Driver, Vehicle

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_add_driver(test_client):
    user = User(username='testuser', email='testuser@example.com', phone_number='+1234567890')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    vehicle = Vehicle(make='Toyota', model='Camry', year=2020, license_plate='ABC123', color='Blue')
    db.session.add(vehicle)
    db.session.commit()

    response = test_client.post('/drivers/add', json={
        'user_id': user.id,
        'license_number': 'ABC123456',
        'vehicle_id': vehicle.id
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Driver added successfully'
    assert 'driver_id' in data

def test_get_driver(test_client):
    driver = Driver.query.first()
    response = test_client.get(f'/drivers/{driver.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['license_number'] == driver.license_number
    assert data['vehicle_id'] == driver.vehicle_id

def test_update_driver(test_client):
    driver = Driver.query.first()
    response = test_client.put('/drivers/update', json={
        'license_number': 'NEW123456'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Driver updated successfully'

    updated_driver = Driver.query.get(driver.id)
    assert updated_driver.license_number == 'NEW123456'

def test_delete_driver(test_client):
    driver = Driver.query.first()
    response = test_client.delete(f'/drivers/{driver.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Driver deleted successfully'

    deleted_driver = Driver.query.get(driver.id)
    assert deleted_driver is None
