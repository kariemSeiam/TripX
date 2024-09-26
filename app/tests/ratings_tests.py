import pytest
from app import create_app
from app.extensions import db
from app.models import User, Rating
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
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

def get_jwt_headers(user):
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

def test_create_rating(test_client, user):
    headers = get_jwt_headers(user)
    data = {
        "driver_id": 1,
        "trip_id": 1,
        "rating": 4.5,
        "feedback": "Great ride!"
    }
    response = test_client.post('/ratings', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Rating created"

def test_get_rating(test_client, user):
    headers = get_jwt_headers(user)
    rating = Rating(
        driver_id=1,
        rider_id=user.id,
        trip_id=1,
        rating=4.5,
        feedback="Great ride!"
    )
    db.session.add(rating)
    db.session.commit()

    response = test_client.get(f'/ratings/{rating.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['rating'] == 4.5

def test_get_ratings(test_client, user):
    headers = get_jwt_headers(user)
    rating = Rating(
        driver_id=1,
        rider_id=user.id,
        trip_id=1,
        rating=4.5,
        feedback="Great ride!"
    )
    db.session.add(rating)
    db.session.commit()

    response = test_client.get('/ratings', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
