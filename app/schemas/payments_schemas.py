from marshmallow import Schema, fields, validate

class PaymentSchema(Schema):
    """Schema for validating payment data."""
    driver_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True, validate=validate.Length(equal=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))

class PaymentUpdateSchema(Schema):
    """Schema for validating payment update data."""
    amount = fields.Float()
    currency = fields.Str(validate=validate.Length(equal=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))
