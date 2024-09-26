from flask import Blueprint, request, jsonify
from app.models import Notification
from app.extensions import db
from app.schemas.notifications_schemas import NotificationSchema, MarkAsReadSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.notifications_utils import log_notification_action

notifications_bp = Blueprint('notifications_bp', __name__)

@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id).all()
    schema = NotificationSchema(many=True)
    return jsonify(schema.dump(notifications)), 200

@notifications_bp.route('/notifications/<int:notification_id>/mark_as_read', methods=['POST'])
@jwt_required()
def mark_notification_as_read(notification_id):
    user_id = get_jwt_identity()
    notification = Notification.query.get(notification_id)
    if not notification or notification.user_id != user_id:
        return jsonify({"message": "Notification not found"}), 404

    notification.read = True
    db.session.commit()
    log_notification_action(notification.id, 'mark_as_read')
    return jsonify({"message": "Notification marked as read"}), 200
