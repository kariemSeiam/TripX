from flask_restful import Resource
from flask import request, jsonify, current_app
from app.models import Vehicle, User
from app.extensions import db
from app.schemas.vehicles_schemas import VehicleSchema, VehicleUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

class VehicleListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        vehicles = Vehicle.query.filter_by(user_id=user_id).all()
        vehicle_schema = VehicleSchema(many=True)
        return vehicle_schema.dump(vehicles), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        schema = VehicleSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400

        new_vehicle = Vehicle(
            user_id=user_id,
            make=data['make'],
            model=data['model'],
            year=data['year'],
            license_plate=data['license_plate'],
            color=data.get('color'),
            vehicle_type=data.get('vehicle_type'),
            photo_urls_list=data.get('vehicle_photo_urls', [])  # Use the property setter
        )
        try:
            db.session.add(new_vehicle)
            db.session.commit()
            return VehicleSchema().dump(new_vehicle), 201
        except Exception as e:
            db.session.rollback()  # Important: Rollback on errors
            current_app.logger.error(f"Error creating vehicle: {e}")
            return jsonify({"message": "Failed to create vehicle"}), 500

class VehicleResource(Resource):
    @jwt_required()
    def get(self, vehicle_id):
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404
        return VehicleSchema().dump(vehicle), 200

    @jwt_required()
    def put(self, vehicle_id):
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        if not vehicle:
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

        try:
            db.session.commit()
            return VehicleSchema().dump(vehicle), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating vehicle: {e}")
            return jsonify({"message": "Failed to update vehicle"}), 500

    @jwt_required()
    def delete(self, vehicle_id):
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404
        try:
            db.session.delete(vehicle)
            db.session.commit()
            return jsonify({"message": "Vehicle deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting vehicle: {e}")
            return jsonify({"message": "Failed to delete vehicle"}), 500
