import pytest
from app import create_app
from app.extensions import db
from app.models import Notification, User
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
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

def get_jwt_headers(user):
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

def test_get_notifications(test_client, user):
    notification = Notification(user_id=user.id, title='Test', message='This is a test notification')
    db.session.add(notification)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get('/notifications', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_mark_notification_as_read(test_client, user):
    notification = Notification(user_id=user.id, title='Test', message='This is a test notification')
    db.session.add(notification)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.post(f'/notifications/{notification.id}/mark_as_read', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Notification marked as read'
