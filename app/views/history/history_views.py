from flask import Blueprint, request, jsonify
from app.models import History
from app.extensions import db
from app.schemas.history_schemas import HistorySchema, CreateHistorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/history', methods=['POST'])
@jwt_required()
def create_history():
    data = request.get_json()
    schema = CreateHistorySchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()
    new_history = History(
        user_id=user_id,
        trip_id=data['trip_id'],
        event_type=data['event_type'],
        description=data.get('description')
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify({"message": "History created"}), 201

@history_bp.route('/history/<int:history_id>', methods=['GET'])
@jwt_required()
def get_history(history_id):
    history = History.query.get(history_id)
    if not history:
        return jsonify({"message": "History not found"}), 404

    schema = HistorySchema()
    return jsonify(schema.dump(history)), 200

@history_bp.route('/history', methods=['GET'])
@jwt_required()
def get_histories():
    user_id = get_jwt_identity()
    histories = History.query.filter_by(user_id=user_id).all()
    schema = HistorySchema(many=True)
    return jsonify(schema.dump(histories)), 200
