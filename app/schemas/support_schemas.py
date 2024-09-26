from marshmallow import Schema, fields, validate

class SupportTicketSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    subject = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class SupportMessageSchema(Schema):
    id = fields.Int(dump_only=True)
    ticket_id = fields.Int(required=True)
    sender_id = fields.Int(required=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    timestamp = fields.DateTime(dump_only=True)

class NewSupportMessageSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1))
