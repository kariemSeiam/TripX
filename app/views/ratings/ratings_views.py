from flask import Blueprint, request, jsonify
from app.models import Rating
from app.extensions import db
from app.schemas.ratings_schemas import RatingSchema, CreateRatingSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

ratings_bp = Blueprint('ratings_bp', __name__)

@ratings_bp.route('/ratings', methods=['POST'])
@jwt_required()
def create_rating():
    data = request.get_json()
    schema = CreateRatingSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    rider_id = get_jwt_identity()
    new_rating = Rating(
        driver_id=data['driver_id'],
        rider_id=rider_id,
        trip_id=data['trip_id'],
        rating=data['rating'],
        feedback=data.get('feedback')
    )
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"message": "Rating created"}), 201

@ratings_bp.route('/ratings/<int:rating_id>', methods=['GET'])
@jwt_required()
def get_rating(rating_id):
    rating = Rating.query.get(rating_id)
    if not rating:
        return jsonify({"message": "Rating not found"}), 404

    schema = RatingSchema()
    return jsonify(schema.dump(rating)), 200

@ratings_bp.route('/ratings', methods=['GET'])
@jwt_required()
def get_ratings():
    ratings = Rating.query.all()
    schema = RatingSchema(many=True)
    return jsonify(schema.dump(ratings)), 200
