from marshmallow import Schema, fields, validate

class ConversationSchema(Schema):
    id = fields.Int(dump_only=True)
    user1_id = fields.Int(required=True)
    user2_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    conversation_id = fields.Int(required=True)
    sender_id = fields.Int(required=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    timestamp = fields.DateTime(dump_only=True)

class NewMessageSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1))
