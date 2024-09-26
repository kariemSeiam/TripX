import pytest
from app import create_app
from app.extensions import db
from app.models import Promotion, User
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

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

def test_create_promotion(test_client, user):
    headers = get_jwt_headers(user)
    data = {
        "description": "10% off on all rides",
        "discount_type": "percent",
        "discount_value": 10.0,
        "start_date": datetime.utcnow().isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "usage_limit": 100
    }
    response = test_client.post('/promotions', json=data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert "promo_code" in data

def test_get_promotion(test_client, user):
    headers = get_jwt_headers(user)
    promotion = Promotion(
        code='PROMO1234',
        description='10% off on all rides',
        discount_type='percent',
        discount_value=10.0,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        usage_limit=100
    )
    db.session.add(promotion)
    db.session.commit()

    response = test_client.get(f'/promotions/{promotion.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 'PROMO1234'

def test_get_promotions(test_client, user):
    headers = get_jwt_headers(user)
    promotion = Promotion(
        code='PROMO1234',
        description='10% off on all rides',
        discount_type='percent',
        discount_value=10.0,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        usage_limit=100
    )
    db.session.add(promotion)
    db.session.commit()

    response = test_client.get('/promotions', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
