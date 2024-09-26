from flask import Blueprint, request, jsonify
from app.models import Document, User
from app.extensions import db
from app.schemas.documents_schemas import DocumentSchema, DocumentStatusSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.documents_utils import save_document_file, allowed_file

documents_bp = Blueprint('documents_bp', __name__)

@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    document_type = request.form.get('document_type')

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_url = save_document_file(file)
        document = Document(
            user_id=user_id,
            document_type=document_type,
            file_url=file_url
        )
        db.session.add(document)
        db.session.commit()
        return jsonify({"message": "Document uploaded successfully", "document_id": document.id}), 201

    return jsonify({"message": "Invalid file type"}), 400

@documents_bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_document_status(document_id):
    document = Document.query.get(document_id)
    if not document:
        return jsonify({"message": "Document not found"}), 404

    schema = DocumentStatusSchema()
    return jsonify(schema.dump(document)), 200
