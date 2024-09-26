import pytest
from app import create_app
from app.extensions import db
from app.models import User, Document

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_upload_document(test_client):
    user = User(username='testuser', email='testuser@example.com', phone_number='+1234567890')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    data = {
        'document_type': 'license',
        'file': (io.BytesIO(b"this is a test"), 'test.jpg')
    }
    response = test_client.post('/documents/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Document uploaded successfully'
    assert 'document_id' in data

def test_get_document_status(test_client):
    document = Document.query.first()
    response = test_client.get(f'/documents/{document.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == document.status
    assert data['document_type'] == document.document_type
