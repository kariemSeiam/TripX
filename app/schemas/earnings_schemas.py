from marshmallow import Schema, fields, validate

class EarningSchema(Schema):
    driver_id = fields.Int(required=True)
    trip_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True, validate=validate.Length(equal=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))

class EarningUpdateSchema(Schema):
    amount = fields.Float(validate=validate.Range(min=0))
    currency = fields.Str(validate=validate.Length(equal=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))
