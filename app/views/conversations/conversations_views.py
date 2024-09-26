from flask import Blueprint, request, jsonify
from app.models import Conversation, Message
from app.extensions import db
from app.schemas.conversations_schemas import ConversationSchema, MessageSchema, NewMessageSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.conversations_utils import log_conversation_action

conversations_bp = Blueprint('conversations_bp', __name__)

@conversations_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()
    conversations = Conversation.query.filter((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)).all()
    schema = ConversationSchema(many=True)
    return jsonify(schema.dump(conversations)), 200

@conversations_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.get(conversation_id)
    if not conversation or (conversation.user1_id != user_id and conversation.user2_id != user_id):
        return jsonify({"message": "Conversation not found"}), 404

    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    schema = MessageSchema(many=True)
    return jsonify(schema.dump(messages)), 200

@conversations_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.get(conversation_id)
    if not conversation or (conversation.user1_id != user_id and conversation.user2_id != user_id):
        return jsonify({"message": "Conversation not found"}), 404

    data = request.get_json()
    schema = NewMessageSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_message = Message(
        conversation_id=conversation_id,
        sender_id=user_id,
        content=data['content']
    )
    db.session.add(new_message)
    db.session.commit()
    log_conversation_action(conversation_id, 'new_message', new_message.id)
    return jsonify({"message": "Message sent"}), 201
