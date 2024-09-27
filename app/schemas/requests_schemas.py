from marshmallow import Schema, fields, validate

class RequestSchema(Schema):
    request_type = fields.Str(required=True, validate=validate.Length(min=1))
    details = fields.Str()

class RequestUpdateSchema(Schema):
    request_type = fields.Str(validate=validate.Length(min=1))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled', 'in_progress']))
    details = fields.Str()
