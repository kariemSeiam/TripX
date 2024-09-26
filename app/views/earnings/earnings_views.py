from flask import Blueprint, request, jsonify
from app.models import Earning, Driver, Trip
from app.extensions import db
from app.schemas.earnings_schemas import EarningSchema, EarningUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

earnings_bp = Blueprint('earnings_bp', __name__)

@earnings_bp.route('/earnings', methods=['POST'])
@jwt_required()
def create_earning():
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    data = request.get_json()
    schema = EarningSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    trip = Trip.query.get(data['trip_id'])
    if not trip or trip.driver_id != driver_id:
        return jsonify({"message": "Trip not found or not associated with driver"}), 404

    new_earning = Earning(
        driver_id=driver.id,
        trip_id=trip.id,
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'pending')
    )
    db.session.add(new_earning)
    db.session.commit()
    return jsonify({"message": "Earning created successfully", "earning_id": new_earning.id}), 201

@earnings_bp.route('/earnings', methods=['GET'])
@jwt_required()
def get_earnings():
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    earnings = Earning.query.filter_by(driver_id=driver.id).all()
    schema = EarningSchema(many=True)
    return jsonify(schema.dump(earnings)), 200

@earnings_bp.route('/earnings/<int:earning_id>', methods=['PUT'])
@jwt_required()
def update_earning(earning_id):
    driver_id = get_jwt_identity()
    earning = Earning.query.get(earning_id)
    if not earning or earning.driver_id != driver_id:
        return jsonify({"message": "Earning not found"}), 404

    data = request.get_json()
    schema = EarningUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    earning.amount = data.get('amount', earning.amount)
    earning.currency = data.get('currency', earning.currency)
    earning.status = data.get('status', earning.status)

    db.session.commit()
    return jsonify({"message": "Earning updated successfully"}), 200

@earnings_bp.route('/earnings/<int:earning_id>', methods=['DELETE'])
@jwt_required()
def delete_earning(earning_id):
    driver_id = get_jwt_identity()
    earning = Earning.query.get(earning_id)
    if not earning or earning.driver_id != driver_id:
        return jsonify({"message": "Earning not found"}), 404

    db.session.delete(earning)
    db.session.commit()
    return jsonify({"message": "Earning deleted successfully"}), 200
