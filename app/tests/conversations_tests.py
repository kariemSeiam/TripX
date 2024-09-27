import pytest
from app import create_app
from app.extensions import db
from app.models import Conversation, Message, User
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

def test_get_conversations(test_client, user):
    conversation = Conversation(user1_id=user.id, user2_id=user.id + 1)
    db.session.add(conversation)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get('/conversations', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_messages(test_client, user):
    conversation = Conversation(user1_id=user.id, user2_id=user.id + 1)
    message = Message(conversation_id=conversation.id, sender_id=user.id, content='Hello')
    db.session.add(conversation)
    db.session.add(message)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get(f'/conversations/{conversation.id}/messages', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_send_message(test_client, user):
    conversation = Conversation(user1_id=user.id, user2_id=user.id + 1)
    db.session.add(conversation)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.post(f'/conversations/{conversation.id}/messages', json={'content': 'Hello'}, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Message sent'
