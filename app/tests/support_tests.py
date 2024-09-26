import pytest
from app import create_app
from app.extensions import db
from app.models import SupportTicket, SupportMessage, User
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

def test_get_tickets(test_client, user):
    ticket = SupportTicket(user_id=user.id, subject='Test Subject', description='Test Description')
    db.session.add(ticket)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get('/support/tickets', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_ticket(test_client, user):
    ticket = SupportTicket(user_id=user.id, subject='Test Subject', description='Test Description')
    db.session.add(ticket)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get(f'/support/tickets/{ticket.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['subject'] == 'Test Subject'

def test_create_ticket(test_client, user):
    headers = get_jwt_headers(user)
    response = test_client.post('/support/tickets', json={'subject': 'New Ticket', 'description': 'Test Description'}, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Ticket created'

def test_get_messages(test_client, user):
    ticket = SupportTicket(user_id=user.id, subject='Test Subject', description='Test Description')
    message = SupportMessage(ticket_id=ticket.id, sender_id=user.id, content='Hello')
    db.session.add(ticket)
    db.session.add(message)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.get(f'/support/tickets/{ticket.id}/messages', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_send_message(test_client, user):
    ticket = SupportTicket(user_id=user.id, subject='Test Subject', description='Test Description')
    db.session.add(ticket)
    db.session.commit()

    headers = get_jwt_headers(user)
    response = test_client.post(f'/support/tickets/{ticket.id}/messages', json={'content': 'Hello'}, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Message sent'
