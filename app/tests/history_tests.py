import pytest
from app import create_app
from app.extensions import db
from app.models import User, History
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

def test_create_history(test_client, user):
    headers = get_jwt_headers(user)
    data = {
        "trip_id": 1,
        "event_type": "ride_completed",
        "description": "Trip completed successfully"
    }
    response = test_client.post('/history', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "History created"

def test_get_history(test_client, user):
    headers = get_jwt_headers(user)
    history = History(
        user_id=user.id,
        trip_id=1,
        event_type="ride_completed",
        description="Trip completed successfully"
    )
    db.session.add(history)
    db.session.commit()

    response = test_client.get(f'/history/{history.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['event_type'] == "ride_completed"

def test_get_histories(test_client, user):
    headers = get_jwt_headers(user)
    history = History(
        user_id=user.id,
        trip_id=1,
        event_type="ride_completed",
        description="Trip completed successfully"
    )
    db.session.add(history)
    db.session.commit()

    response = test_client.get('/history', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
