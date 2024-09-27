import pytest
from app import create_app
from app.extensions import db
from app.models import Driver, Withdrawal
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
def driver():
    driver = Driver(username='testdriver', email='testdriver@example.com', phone_number='+1234567890')
    driver.set_password('password')
    db.session.add(driver)
    db.session.commit()
    return driver

def get_jwt_headers(driver):
    token = create_access_token(identity=driver.id)
    return {'Authorization': f'Bearer {token}'}

def test_create_withdrawal(test_client, driver):
    headers = get_jwt_headers(driver)
    data = {
        'amount': 100.00,
        'method': 'bank_transfer'
    }
    response = test_client.post('/withdrawals', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Withdrawal request created successfully'
    assert 'withdrawal_id' in data

def test_get_withdrawals(test_client, driver):
    withdrawal = Withdrawal(driver_id=driver.id, amount=100.00, method='bank_transfer')
    db.session.add(withdrawal)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.get('/withdrawals', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_withdrawal(test_client, driver):
    withdrawal = Withdrawal(driver_id=driver.id, amount=100.00, method='bank_transfer')
    db.session.add(withdrawal)
    db.session.commit()

    headers = get_jwt_headers(driver)
    data = {
        'status': 'processed'
    }
    response = test_client.put(f'/withdrawals/{withdrawal.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Withdrawal updated successfully'

def test_delete_withdrawal(test_client, driver):
    withdrawal = Withdrawal(driver_id=driver.id, amount=100.00, method='bank_transfer')
    db.session.add(withdrawal)
    db.session.commit()

    headers = get_jwt_headers(driver)
    response = test_client.delete(f'/withdrawals/{withdrawal.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Withdrawal deleted successfully'
