
from marshmallow import Schema, fields

class ReferralSchema(Schema):
    id = fields.Int(dump_only=True)
    referrer_id = fields.Int(dump_only=True)
    referred_id = fields.Int(dump_only=True)
    referral_code = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CreateReferralSchema(Schema):
    pass  # No input fields needed for creating a referral
