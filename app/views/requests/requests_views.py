from flask import Blueprint, request, jsonify
from app.models import Request, User
from app.extensions import db
from app.schemas.requests_schemas import RequestSchema, RequestUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

requests_bp = Blueprint('requests_bp', __name__)

@requests_bp.route('/requests', methods=['POST'])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    schema = RequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_request = Request(
        user_id=user_id,
        request_type=data['request_type'],
        details=data.get('details')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Request created successfully", "request_id": new_request.id}), 201

@requests_bp.route('/requests', methods=['GET'])
@jwt_required()
def get_requests():
    user_id = get_jwt_identity()
    requests = Request.query.filter_by(user_id=user_id).all()
    schema = RequestSchema(many=True)
    return jsonify(schema.dump(requests)), 200

@requests_bp.route('/requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_request(request_id):
    user_id = get_jwt_identity()
    req = Request.query.get(request_id)
    if not req or req.user_id != user_id:
        return jsonify({"message": "Request not found"}), 404

    data = request.get_json()
    schema = RequestUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    req.request_type = data.get('request_type', req.request_type)
    req.status = data.get('status', req.status)
    req.details = data.get('details', req.details)

    db.session.commit()
    return jsonify({"message": "Request updated successfully"}), 200

@requests_bp.route('/requests/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    user_id = get_jwt_identity()
    req = Request.query.get(request_id)
    if not req or req.user_id != user_id:
        return jsonify({"message": "Request not found"}), 404

    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Request deleted successfully"}), 200
