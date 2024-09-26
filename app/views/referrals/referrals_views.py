from flask import Blueprint, request, jsonify
from app.models import Referral
from app.extensions import db
from app.schemas.referrals_schemas import ReferralSchema, CreateReferralSchema
from app.utils.referrals_utils import generate_referral_code
from flask_jwt_extended import jwt_required, get_jwt_identity

referrals_bp = Blueprint('referrals_bp', __name__)

@referrals_bp.route('/referrals', methods=['POST'])
@jwt_required()
def create_referral():
    user_id = get_jwt_identity()
    data = request.get_json()
    schema = CreateReferralSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    referral_code = generate_referral_code(user_id)
    new_referral = Referral(
        referrer_id=user_id,
        referral_code=referral_code
    )
    db.session.add(new_referral)
    db.session.commit()

    return jsonify({"message": "Referral created", "referral_code": referral_code}), 201

@referrals_bp.route('/referrals/<int:referral_id>', methods=['GET'])
@jwt_required()
def get_referral(referral_id):
    user_id = get_jwt_identity()
    referral = Referral.query.get(referral_id)
    if not referral or referral.referrer_id != user_id:
        return jsonify({"message": "Referral not found"}), 404

    schema = ReferralSchema()
    return jsonify(schema.dump(referral)), 200

@referrals_bp.route('/referrals', methods=['GET'])
@jwt_required()
def get_referrals():
    user_id = get_jwt_identity()
    referrals = Referral.query.filter_by(referrer_id=user_id).all()
    schema = ReferralSchema(many=True)
    return jsonify(schema.dump(referrals)), 200
