from marshmallow import Schema, fields, validate

class DriverSchema(Schema):
    user_id = fields.Int(required=True)
    license_number = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    vehicle_id = fields.Int(required=True)

class DriverUpdateSchema(Schema):
    license_number = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    vehicle_id = fields.Int(required=False)
