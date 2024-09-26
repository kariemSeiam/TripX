from flask import Blueprint, request, jsonify
from app.models import User, Driver, Vehicle
from app.extensions import db
from app.schemas.drivers_schemas import DriverSchema, DriverUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

drivers_bp = Blueprint('drivers_bp', __name__)

@drivers_bp.route('/add', methods=['POST'])
@jwt_required()
def add_driver():
    schema = DriverSchema()
    data = schema.load(request.get_json())
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    driver = Driver(
        user_id=user_id,
        license_number=data['license_number'],
        vehicle_id=data['vehicle_id']
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({"message": "Driver added successfully", "driver_id": driver.id}), 201

@drivers_bp.route('/<int:driver_id>', methods=['GET'])
@jwt_required()
def get_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    schema = DriverSchema()
    return jsonify(schema.dump(driver)), 200

@drivers_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_driver():
    schema = DriverUpdateSchema()
    data = schema.load(request.get_json())
    user_id = get_jwt_identity()
    driver = Driver.query.filter_by(user_id=user_id).first()

    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    if 'license_number' in data:
        driver.license_number = data['license_number']
    if 'vehicle_id' in data:
        vehicle = Vehicle.query.get(data['vehicle_id'])
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404
        driver.vehicle_id = data['vehicle_id']

    db.session.commit()
    return jsonify({"message": "Driver updated successfully"}), 200

@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
@jwt_required()
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": "Driver deleted successfully"}), 200
