from marshmallow import Schema, fields, validate

class VehicleSchema(Schema):
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Int(required=True, validate=validate.Range(min=1886, max=2100))
    license_plate = fields.Str(required=True)
    color = fields.Str()
    vehicle_type = fields.Str()
    vehicle_photo_urls = fields.List(fields.Str(), required=False)

class VehicleUpdateSchema(Schema):
    make = fields.Str()
    model = fields.Str()
    year = fields.Int(validate=validate.Range(min=1886, max=2100))
    license_plate = fields.Str()
    color = fields.Str()
    vehicle_type = fields.Str()
    vehicle_photo_urls = fields.List(fields.Str(), required=False)
