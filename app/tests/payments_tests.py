import pytest
from app import create_app
from app.extensions import db
from app.models import Driver, Payment
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

def get_jwt_headers(driver):
    token = create_access_token(identity=driver.id)
    return {'Authorization': f'Bearer {token}'}

def test_create_payment(test_client, driver):
    headers = get_jwt_headers(driver)
    data = {
        'amount': 100.00,
        'currency': 'USD'
    }
    response = test_client.post('/payments', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Payment created successfully'
    assert 'payment_id' in data

def test_get_payments(test_client, driver):
    payment = Payment(driver_id=driver.id, amount=100.00, currency='USD')
    db.session.add(payment)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.get('/payments', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_payment(test_client, driver):
    payment = Payment(driver_id=driver.id, amount=100.00, currency='USD')
    db.session.add(payment)
    db.session.commit()

    headers = get_jwt_headers(driver)
    data = {
        'status': 'completed'
    }
    response = test_client.put(f'/payments/{payment.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Payment updated successfully'

def test_delete_payment(test_client, driver):
    payment = Payment(driver_id=driver.id, amount=100.00, currency='USD')
    db.session.add(payment)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.delete(f'/payments/{payment.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Payment deleted successfully'
