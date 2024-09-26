from marshmallow import Schema, fields, validate

class TripSchema(Schema):
    rider_id = fields.Int(required=True)
    driver_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    start_location = fields.Str(required=True, validate=validate.Length(min=1))
    end_location = fields.Str(required=True, validate=validate.Length(min=1))
    fare = fields.Float(required=True)
    status = fields.Str(validate=validate.OneOf(['requested', 'started', 'completed', 'cancelled']))

class TripUpdateSchema(Schema):
    start_location = fields.Str(validate=validate.Length(min=1))
    end_location = fields.Str(validate=validate.Length(min=1))
    fare = fields.Float()
    status = fields.Str(validate=validate.OneOf(['requested', 'started', 'completed', 'cancelled']))
