import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_signup(test_client):
    response = test_client.post('/auth/signup', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'phone_number': '+1234567890',
        'password': 'password'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Account created. Verification email sent.'

def test_verify(test_client):
    user = User.query.filter_by(email='testuser@example.com').first()
    token = generate_verification_token(user.email)
    response = test_client.post('/auth/verify', json={'token': token})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Account verified.'

def test_login(test_client):
    response = test_client.post('/auth/login', json={
        'email': 'testuser@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_forgot_password(test_client):
    response = test_client.post('/auth/forgot_password', json={'email': 'testuser@example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Password reset email sent.'

def test_reset_password(test_client):
    user = User.query.filter_by(email='testuser@example.com').first()
    token = generate_password_reset_token(user.email)
    response = test_client.post('/auth/reset_password', json={
        'token': token,
        'new_password': 'newpassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Password reset successful'

def test_logout(test_client):
    response = test_client.post('/auth/logout')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Logged out successfully'
