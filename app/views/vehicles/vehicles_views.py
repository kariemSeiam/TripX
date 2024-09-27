from flask import Blueprint, request, jsonify
from app.models import Vehicle, User
from app.extensions import db
from app.schemas.vehicles_schemas import VehicleSchema, VehicleUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

vehicles_bp = Blueprint('vehicles_bp', __name__)

@vehicles_bp.route('/vehicles', methods=['POST'])
@jwt_required()
def add_vehicle():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    schema = VehicleSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check for existing vehicle with the same license plate
    existing_vehicle = Vehicle.query.filter_by(license_plate=data['license_plate']).first()
    if existing_vehicle:
        return jsonify({"message": "A vehicle with this license plate already exists."}), 400

    vehicle = Vehicle(
        user_id=user_id,
        make=data['make'],
        model=data['model'],
        year=data['year'],
        license_plate=data['license_plate'],
        color=data.get('color'),
        vehicle_type=data.get('vehicle_type'),
        photo_urls_list=data.get('vehicle_photo_urls', [])
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle added successfully", "vehicle_id": vehicle.id}), 201

@vehicles_bp.route('/vehicles', methods=['GET'])
@jwt_required()
def get_vehicles():
    user_id = get_jwt_identity()
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    schema = VehicleSchema(many=True)
    return jsonify(schema.dump(vehicles)), 200

@vehicles_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    user_id = get_jwt_identity()
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle or vehicle.user_id != user_id:
        return jsonify({"message": "Vehicle not found"}), 404

    data = request.get_json()
    schema = VehicleUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    vehicle.license_plate = data.get('license_plate', vehicle.license_plate)
    vehicle.color = data.get('color', vehicle.color)
    vehicle.vehicle_type = data.get('vehicle_type', vehicle.vehicle_type)
    vehicle.photo_urls_list = data.get('vehicle_photo_urls', vehicle.photo_urls_list)  # Use the property setter

    db.session.commit()
    return jsonify({"message": "Vehicle updated successfully"}), 200

@vehicles_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    user_id = get_jwt_identity()
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle or vehicle.user_id != user_id:
        return jsonify({"message": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted successfully"}), 200
