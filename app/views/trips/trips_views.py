from flask import Blueprint, request, jsonify
from app.models import Trip, User, Driver, Vehicle
from app.extensions import db
from app.schemas.trips_schemas import TripSchema, TripUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

trips_bp = Blueprint('trips_bp', __name__)

@trips_bp.route('/trips', methods=['POST'])
@jwt_required()
def create_trip():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    schema = TripSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    driver = Driver.query.get(vehicle.driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    new_trip = Trip(
        driver_id=driver.id,
        rider_id=user.id,
        vehicle_id=vehicle.id,
        start_location=data['start_location'],
        end_location=data['end_location'],
        fare=data['fare']
    )
    db.session.add(new_trip)
    db.session.commit()
    return jsonify({"message": "Trip created successfully", "trip_id": new_trip.id}), 201

@trips_bp.route('/trips', methods=['GET'])
@jwt_required()
def get_trips():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    trips = Trip.query.filter_by(rider_id=user.id).all()
    schema = TripSchema(many=True)
    return jsonify(schema.dump(trips)), 200

@trips_bp.route('/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.get(trip_id)
    if not trip or trip.rider_id != user_id:
        return jsonify({"message": "Trip not found"}), 404

    data = request.get_json()
    schema = TripUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    trip.start_location = data.get('start_location', trip.start_location)
    trip.end_location = data.get('end_location', trip.end_location)
    trip.fare = data.get('fare', trip.fare)
    trip.status = data.get('status', trip.status)

    db.session.commit()
    return jsonify({"message": "Trip updated successfully"}), 200

@trips_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.get(trip_id)
    if not trip or trip.rider_id != user_id:
        return jsonify({"message": "Trip not found"}), 404

    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted successfully"}), 200
