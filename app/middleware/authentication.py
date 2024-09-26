from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return f(*args, **kwargs)
    return decorated_function

from flask_jwt_extended import JWTManager

class Authentication:
    def __init__(self, app=None):
        self.jwt = JWTManager()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.jwt.init_app(app)
