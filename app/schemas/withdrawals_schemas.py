from marshmallow import Schema, fields, validate

class WithdrawalSchema(Schema):
    driver_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    method = fields.Str(required=True, validate=validate.Length(min=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'processed', 'failed']))

class WithdrawalUpdateSchema(Schema):
    amount = fields.Float()
    method = fields.Str(validate=validate.Length(min=3))
    status = fields.Str(validate=validate.OneOf(['pending', 'processed', 'failed']))
