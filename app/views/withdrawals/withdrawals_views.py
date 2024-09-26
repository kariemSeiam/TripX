from flask import Blueprint, request, jsonify
from app.models import Withdrawal, Driver
from app.extensions import db
from app.schemas.withdrawals_schemas import WithdrawalSchema, WithdrawalUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.withdrawals_utils import log_withdrawal_action

withdrawals_bp = Blueprint('withdrawals_bp', __name__)

@withdrawals_bp.route('/withdrawals', methods=['POST'])
@jwt_required()
def create_withdrawal():
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    data = request.get_json()
    schema = WithdrawalSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_withdrawal = Withdrawal(
        driver_id=driver.id,
        amount=data['amount'],
        method=data['method'],
        status=data.get('status', 'pending')
    )
    db.session.add(new_withdrawal)
    db.session.commit()

    log_withdrawal_action(new_withdrawal.id, 'create')
    return jsonify({"message": "Withdrawal request created successfully", "withdrawal_id": new_withdrawal.id}), 201

@withdrawals_bp.route('/withdrawals', methods=['GET'])
@jwt_required()
def get_withdrawals():
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    withdrawals = Withdrawal.query.filter_by(driver_id=driver.id).all()
    schema = WithdrawalSchema(many=True)
    return jsonify(schema.dump(withdrawals)), 200

@withdrawals_bp.route('/withdrawals/<int:withdrawal_id>', methods=['PUT'])
@jwt_required()
def update_withdrawal(withdrawal_id):
    driver_id = get_jwt_identity()
    withdrawal = Withdrawal.query.get(withdrawal_id)
    if not withdrawal or withdrawal.driver_id != driver_id:
        return jsonify({"message": "Withdrawal not found"}), 404

    data = request.get_json()
    schema = WithdrawalUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    withdrawal.amount = data.get('amount', withdrawal.amount)
    withdrawal.method = data.get('method', withdrawal.method)
    withdrawal.status = data.get('status', withdrawal.status)

    db.session.commit()
    log_withdrawal_action(withdrawal.id, 'update')
    return jsonify({"message": "Withdrawal updated successfully"}), 200

@withdrawals_bp.route('/withdrawals/<int:withdrawal_id>', methods=['DELETE'])
@jwt_required()
def delete_withdrawal(withdrawal_id):
    driver_id = get_jwt_identity()
    withdrawal = Withdrawal.query.get(withdrawal_id)
    if not withdrawal or withdrawal.driver_id != driver_id:
        return jsonify({"message": "Withdrawal not found"}), 404

    db.session.delete(withdrawal)
    db.session.commit()
    log_withdrawal_action(withdrawal.id, 'delete')
    return jsonify({"message": "Withdrawal deleted successfully"}), 200
