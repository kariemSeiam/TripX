from marshmallow import Schema, fields

class PromotionSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(dump_only=True)
    description = fields.Str()
    discount_type = fields.Str()
    discount_value = fields.Float()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    usage_limit = fields.Int()
    times_used = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CreatePromotionSchema(Schema):
    description = fields.Str(required=True)
    discount_type = fields.Str(required=True)
    discount_value = fields.Float(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    usage_limit = fields.Int(required=True)
