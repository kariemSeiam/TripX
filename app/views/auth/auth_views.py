from flask import Blueprint, request, jsonify, current_app
from app.models import User, TokenBlacklist
from app.extensions import db, jwt
from app.schemas.auth_schemas import UserSchema, LoginSchema, PasswordResetSchema
from app.services.email_service import send_verification_email, send_password_reset_email
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jti
)
from app.utils.auth_utils import (
    generate_verification_token, confirm_verification_token,
    generate_password_reset_token, confirm_password_reset_token
)
from datetime import datetime, timedelta

auth_bp = Blueprint('auth_bp', __name__)

import random
from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app.extensions import db
from app.schemas.auth_schemas import UserSchema

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    schema = UserSchema()

    # Log the incoming JSON request
    current_app.logger.info(f"Incoming signup data: {request.get_json()}")

    try:
        data = schema.load(request.get_json())
    except Exception as e:
        current_app.logger.error(f"Signup validation error: {e}")
        return jsonify({"error": str(e)}), 400

    # Check if the user already exists
    existing_user = User.query.filter((User.email == data['email']) | (User.phone_number == data['phone_number'])).first()
    if existing_user:
        return jsonify({"error": "A user with this email or phone number already exists."}), 400

    # Generate a verification code
    verification_code = str(random.randint(100000, 999999))  # Generate a 6-digit code

    user = User(
        username=data['username'],
        email=data['email'],
        phone_number=data['phone_number'],
        verification_code=verification_code,
        is_verified = True  # Store the verification code
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    # Optionally send the verification code via email/SMS
    # send_verification_code(user.email, verification_code)

    return jsonify({"message": "Account created. Please verify your account using the code sent to your email."}), 201

@auth_bp.route('/verify', methods=['POST'])
def verify():
    token = request.json.get('token')
    email = confirm_verification_token(token)
    if not email:
        return jsonify({"message": "Invalid or expired token"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.is_verified = True
    db.session.commit()
    return jsonify({"message": "Account verified"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        current_app.logger.error(f"Login validation error: {e}")
        return jsonify({"error": str(e)}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    if not user.is_verified:
        return jsonify({"message": "Account not verified"}), 403

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token, "expires_in": 3600}), 200

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    send_password_reset_email(user.email, generate_password_reset_token(user.email))
    return jsonify({"message": "Password reset email sent"}), 200

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    schema = PasswordResetSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        current_app.logger.error(f"Password reset validation error: {e}")
        return jsonify({"error": str(e)}), 400

    email = confirm_password_reset_token(data['token'])
    if not email:
        return jsonify({"message": "Invalid or expired token"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.set_password(data['new_password'])
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jti(request.headers.get('Authorization').split()[1])
    token_type = 'access'
    user_identity = get_jwt_identity()
    expires = datetime.utcnow() + timedelta(hours=1)  # Assuming token expires in 1 hour

    blacklisted_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        revoked=True,
        expires=expires
    )
    db.session.add(blacklisted_token)
    db.session.commit()
    return jsonify({"message": "Successfully logged out"}), 200
