from flask import Blueprint, request, jsonify
from app.models import Promotion
from app.extensions import db
from app.schemas.promotions_schemas import PromotionSchema, CreatePromotionSchema
from app.utils.promotions_utils import generate_promo_code
from flask_jwt_extended import jwt_required, get_jwt_identity

promotions_bp = Blueprint('promotions_bp', __name__)

@promotions_bp.route('/promotions', methods=['POST'])
@jwt_required()
def create_promotion():
    data = request.get_json()
    schema = CreatePromotionSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    promo_code = generate_promo_code()
    new_promotion = Promotion(
        code=promo_code,
        description=data['description'],
        discount_type=data['discount_type'],
        discount_value=data['discount_value'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        usage_limit=data['usage_limit']
    )
    db.session.add(new_promotion)
    db.session.commit()

    return jsonify({"message": "Promotion created", "promo_code": promo_code}), 201

@promotions_bp.route('/promotions/<int:promotion_id>', methods=['GET'])
@jwt_required()
def get_promotion(promotion_id):
    promotion = Promotion.query.get(promotion_id)
    if not promotion:
        return jsonify({"message": "Promotion not found"}), 404

    schema = PromotionSchema()
    return jsonify(schema.dump(promotion)), 200

@promotions_bp.route('/promotions', methods=['GET'])
@jwt_required()
def get_promotions():
    promotions = Promotion.query.all()
    schema = PromotionSchema(many=True)
    return jsonify(schema.dump(promotions)), 200
