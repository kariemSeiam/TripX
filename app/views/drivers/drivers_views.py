from flask import Blueprint, request, jsonify, current_app
from app.models import User, Driver, Vehicle
from app.extensions import db
from app.schemas.drivers_schemas import DriverSchema, DriverUpdateSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from marshmallow import ValidationError
import logging

drivers_bp = Blueprint('drivers_bp', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Register a new driver account
@drivers_bp.route('/register', methods=['POST'])
def register_driver():
    current_app.logger.info("Registering a new driver.")
    schema = DriverSchema()

    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        current_app.logger.error(f"Driver registration error: {e.messages}")
        return jsonify({"error": "Invalid input", "details": e.messages}), 400

    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Check if vehicle exists
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    # Create new driver
    driver = Driver(
        user_id=data['user_id'],
        license_number=data['license_number'],
        vehicle_id=data['vehicle_id']
    )
    db.session.add(driver)
    db.session.commit()
    current_app.logger.info(f"Driver registered successfully: {driver.id}")

    return jsonify({"message": "Driver registered successfully", "driver_id": driver.id}), 201

# Login driver and create JWT token
@drivers_bp.route('/login', methods=['POST'])
def login_driver():
    current_app.logger.info("Driver attempting to log in.")
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        current_app.logger.info(f"Driver logged in successfully: {user.id}")
        return jsonify({"access_token": access_token}), 200

    current_app.logger.warning("Invalid login attempt.")
    return jsonify({"error": "Invalid credentials"}), 401

# Add a new driver (if not registered)
@drivers_bp.route('/add', methods=['POST'])
@jwt_required()
def add_driver():
    current_app.logger.info("Adding a new driver.")
    schema = DriverSchema()

    data = schema.load(request.get_json())
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    # Check if driver already exists
    existing_driver = Driver.query.filter_by(user_id=user_id).first()
    if existing_driver:
        return jsonify({"error": "Driver already registered."}), 400

    driver = Driver(
        user_id=user_id,
        license_number=data['license_number'],
        vehicle_id=data['vehicle_id']
    )
    db.session.add(driver)
    db.session.commit()
    current_app.logger.info(f"Driver added successfully: {driver.id}")

    return jsonify({"message": "Driver added successfully", "driver_id": driver.id}), 201

# Retrieve a driver's information
@drivers_bp.route('/<int:driver_id>', methods=['GET'])
@jwt_required()
def get_driver(driver_id):
    current_app.logger.info(f"Retrieving information for driver ID: {driver_id}")
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found."}), 404

    schema = DriverSchema()
    return jsonify(schema.dump(driver)), 200

# Update driver's information
@drivers_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_driver():
    current_app.logger.info("Updating driver information.")
    schema = DriverUpdateSchema()

    data = schema.load(request.get_json())
    user_id = get_jwt_identity()
    driver = Driver.query.filter_by(user_id=user_id).first()

    if not driver:
        return jsonify({"error": "Driver not found."}), 404

    if 'license_number' in data:
        driver.license_number = data['license_number']
    if 'vehicle_id' in data:
        vehicle = Vehicle.query.get(data['vehicle_id'])
        if not vehicle:
            return jsonify({"error": "Vehicle not found."}), 404
        driver.vehicle_id = data['vehicle_id']

    db.session.commit()
    current_app.logger.info(f"Driver updated successfully: {driver.id}")

    return jsonify({"message": "Driver updated successfully."}), 200

# Delete a driver
@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
@jwt_required()
def delete_driver(driver_id):
    current_app.logger.info(f"Deleting driver ID: {driver_id}")
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found."}), 404

    db.session.delete(driver)
    db.session.commit()
    current_app.logger.info(f"Driver deleted successfully: {driver.id}")

    return jsonify({"message": "Driver deleted successfully."}), 200
