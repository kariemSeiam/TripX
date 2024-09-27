import pytest
from app import create_app
from app.extensions import db
from app.models import User, Request
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

def test_create_request(test_client, user):
    headers = get_jwt_headers(user)
    data = {
        'request_type': 'ride_request',
        'details': 'Need a ride to the airport.'
    }
    response = test_client.post('/requests', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Request created successfully'
    assert 'request_id' in data

def test_get_requests(test_client, user):
    headers = get_jwt_headers(user)
    response = test_client.get('/requests', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_update_request(test_client, user):
    req = Request(user_id=user.id, request_type='ride_request', details='Need a ride to the airport.')
    db.session.add(req)
    db.session.commit()

    headers = get_jwt_headers(user)
    data = {
        'status': 'completed'
    }
    response = test_client.put(f'/requests/{req.id}', json=data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Request updated successfully'

    # Test invalid status update
    data = {
        'status': 'invalid_status'
    }
    response = test_client.put(f'/requests/{req.id}', json=data, headers=headers)
    assert response.status_code == 400

def test_delete_request(test_client, user):
    req = Request(user_id=user.id, request_type='ride_request', details='Need a ride to the airport.')
    db.session.add(req)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.delete(f'/requests/{req.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Request deleted successfully'
