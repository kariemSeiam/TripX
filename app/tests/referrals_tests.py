import pytest
from app import create_app
from app.extensions import db
from app.models import User, Referral
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

def test_create_referral(test_client, user):
    headers = get_jwt_headers(user)
    response = test_client.post('/referrals', headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert "referral_code" in data

def test_get_referral(test_client, user):
    headers = get_jwt_headers(user)
    referral = Referral(referrer_id=user.id, referral_code='123ABC')
    db.session.add(referral)
    db.session.commit()

    response = test_client.get(f'/referrals/{referral.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['referral_code'] == '123ABC'

def test_get_referrals(test_client, user):
    headers = get_jwt_headers(user)
    referral = Referral(referrer_id=user.id, referral_code='123ABC')
    db.session.add(referral)
    db.session.commit()

    response = test_client.get('/referrals', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
