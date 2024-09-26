from flask import Blueprint, request, jsonify
from app.models import SupportTicket, SupportMessage
from app.extensions import db
from app.schemas.support_schemas import SupportTicketSchema, SupportMessageSchema, NewSupportMessageSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.support_utils import log_support_action

support_bp = Blueprint('support_bp', __name__)

@support_bp.route('/support/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    user_id = get_jwt_identity()
    tickets = SupportTicket.query.filter_by(user_id=user_id).all()
    schema = SupportTicketSchema(many=True)
    return jsonify(schema.dump(tickets)), 200

@support_bp.route('/support/tickets/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    user_id = get_jwt_identity()
    ticket = SupportTicket.query.get(ticket_id)
    if not ticket or ticket.user_id != user_id:
        return jsonify({"message": "Ticket not found"}), 404

    schema = SupportTicketSchema()
    return jsonify(schema.dump(ticket)), 200

@support_bp.route('/support/tickets/<int:ticket_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(ticket_id):
    user_id = get_jwt_identity()
    ticket = SupportTicket.query.get(ticket_id)
    if not ticket or ticket.user_id != user_id:
        return jsonify({"message": "Ticket not found"}), 404

    messages = SupportMessage.query.filter_by(ticket_id=ticket_id).all()
    schema = SupportMessageSchema(many=True)
    return jsonify(schema.dump(messages)), 200

@support_bp.route('/support/tickets/<int:ticket_id>/messages', methods=['POST'])
@jwt_required()
def send_message(ticket_id):
    user_id = get_jwt_identity()
    ticket = SupportTicket.query.get(ticket_id)
    if not ticket or ticket.user_id != user_id:
        return jsonify({"message": "Ticket not found"}), 404

    data = request.get_json()
    schema = NewSupportMessageSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_message = SupportMessage(
        ticket_id=ticket_id,
        sender_id=user_id,
        content=data['content']
    )
    db.session.add(new_message)
    db.session.commit()
    log_support_action(ticket_id, 'new_message', new_message.id)
    return jsonify({"message": "Message sent"}), 201

@support_bp.route('/support/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    user_id = get_jwt_identity()
    data = request.get_json()
    schema = SupportTicketSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_ticket = SupportTicket(
        user_id=user_id,
        subject=data['subject'],
        description=data['description']
    )
    db.session.add(new_ticket)
    db.session.commit()
    log_support_action(new_ticket.id, 'ticket_created')
    return jsonify({"message": "Ticket created", "ticket_id": new_ticket.id}), 201
