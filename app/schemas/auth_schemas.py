from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone_number = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=6))

    
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class PasswordResetSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))
