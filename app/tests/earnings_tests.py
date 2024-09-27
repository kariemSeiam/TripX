import pytest
from app import create_app
from app.extensions import db
from app.models import Driver, Earning, Trip
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
def driver():
    driver = Driver(username='testdriver', email='testdriver@example.com', phone_number='+1234567890')
    driver.set_password('password')
    db.session.add(driver)
    db.session.commit()
    return driver

@pytest.fixture
def trip(driver):
    trip = Trip(driver_id=driver.id, rider_id=1, vehicle_id=1, start_location='123 Main St', end_location='456 Elm St', fare=20.50)
    db.session.add(trip)
    db.session.commit()
    return trip

def get_jwt_headers(driver):
    token = create_access_token(identity=driver.id)
    return {'Authorization': f'Bearer {token}'}

def test_create_earning(test_client, driver, trip):
    headers = get_jwt_headers(driver)
    data = {
        'trip_id': trip.id,
        'amount': 20.50,
        'currency': 'USD'
    }
    response = test_client.post('/earnings', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Earning created successfully'
    assert 'earning_id' in data

def test_get_earnings(test_client, driver, trip):
    earning = Earning(driver_id=driver.id, trip_id=trip.id, amount=20.50, currency='USD')
    db.session.add(earning)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.get('/earnings', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(e['trip_id'] == trip.id for e in data)

def test_update_earning(test_client, driver, trip):
    earning = Earning(driver_id=driver.id, trip_id=trip.id, amount=20.50, currency='USD')
    db.session.add(earning)
    db.session.commit()

    headers = get_jwt_headers(driver)
    data = {
        'status': 'completed'
    }
    response = test_client.put(f'/earnings/{earning.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Earning updated successfully'

def test_delete_earning(test_client, driver, trip):
    earning = Earning(driver_id=driver.id, trip_id=trip.id, amount=20.50, currency='USD')
    db.session.add(earning)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.delete(f'/earnings/{earning.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Earning deleted successfully'
