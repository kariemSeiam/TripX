from flask import Blueprint, request, jsonify
from app.models import Payment, Driver
from app.extensions import db
from app.schemas.payments_schemas import PaymentSchema, PaymentUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

payments_bp = Blueprint('payments_bp', __name__)

@payments_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    """Create a new payment."""
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        logging.error("Driver not found")
        return jsonify({"message": "Driver not found"}), 404

    data = request.get_json()
    schema = PaymentSchema()
    errors = schema.validate(data)
    if errors:
        logging.error(f"Validation errors: {errors}")
        return jsonify(errors), 400

    new_payment = Payment(
        driver_id=driver.id,
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'pending')
    )
    db.session.add(new_payment)
    db.session.commit()
    logging.info(f"Payment created: {new_payment.id}")
    return jsonify({"message": "Payment created successfully", "payment_id": new_payment.id}), 201

@payments_bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    """Retrieve all payments for the current driver."""
    driver_id = get_jwt_identity()
    driver = Driver.query.get(driver_id)
    if not driver:
        logging.error("Driver not found")
        return jsonify({"message": "Driver not found"}), 404

    payments = Payment.query.filter_by(driver_id=driver.id).all()
    schema = PaymentSchema(many=True)
    logging.info(f"Payments retrieved for driver {driver_id}")
    return jsonify(schema.dump(payments)), 200

@payments_bp.route('/payments/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update_payment(payment_id):
    """Update an existing payment."""
    driver_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    if not payment or payment.driver_id != driver_id:
        logging.error("Payment not found")
        return jsonify({"message": "Payment not found"}), 404

    data = request.get_json()
    schema = PaymentUpdateSchema()
    errors = schema.validate(data)
    if errors:
        logging.error(f"Validation errors: {errors}")
        return jsonify(errors), 400

    payment.amount = data.get('amount', payment.amount)
    payment.currency = data.get('currency', payment.currency)
    payment.status = data.get('status', payment.status)

    db.session.commit()
    logging.info(f"Payment updated: {payment.id}")
    return jsonify({"message": "Payment updated successfully"}), 200

@payments_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    """Delete a payment."""
    driver_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    if not payment or payment.driver_id != driver_id:
        logging.error("Payment not found")
        return jsonify({"message": "Payment not found"}), 404

    db.session.delete(payment)
    db.session.commit()
    logging.info(f"Payment deleted: {payment.id}")
    return jsonify({"message": "Payment deleted successfully"}), 200
