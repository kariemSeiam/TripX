from flask_restful import Resource
from flask import request, jsonify, current_app
from app.models import User
from app.extensions import db
from app.schemas.auth_schemas import UserSchema

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username, 'email': user.email}, 200

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email}, 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'email': user.email} for user in users], 200

    def post(self):
        schema = UserSchema()
        data = request.get_json()
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            phone_number=data.get('phone_number')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"User {new_user.username} created successfully.")
        return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}, 201

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email}, 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
